# ----------------------------------------------------------------------
# metrics service
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from dataclasses import dataclass
from typing import Any, Dict, Tuple, Optional

# Third-party modules
import orjson

# NOC modules
from noc.core.service.fastapi import FastAPIService
from noc.core.liftbridge.message import Message
from noc.pm.models.metricscope import MetricScope
from noc.core.cdag.node.base import BaseCDAGNode
from noc.core.cdag.graph import CDAG
from noc.core.cdag.factory.scope import MetricScopeCDAGFactory

MetricKey = Tuple[str, Tuple[Tuple[str, Any], ...], Tuple[str, ...]]


@dataclass
class ScopeInfo(object):
    scope: str
    key_fields: Tuple[str]
    key_labels: Tuple[str]
    units: Dict[str, str]


@dataclass
class Card(object):
    probes: Dict[str, BaseCDAGNode]
    senders: Tuple[BaseCDAGNode]


class MetricsService(FastAPIService):
    name = "metrics"
    use_mongo = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scopes: Dict[str, ScopeInfo] = {}
        self.scope_cdag: Dict[str, CDAG] = {}
        self.cards: Dict[MetricKey, Card] = {}
        self.graph = CDAG("metrics", state=self.get_state())

    async def on_activate(self):
        self.slot_number, self.total_slots = await self.acquire_slot()
        await self.subscribe_stream("metrics", self.slot_number, self.on_metrics)

    async def on_metrics(self, msg: Message) -> None:
        data = orjson.loads(msg.value)
        for item in data:
            scope = item.get("scope")
            if not scope:
                return  # Discard metric without scope
            si = self.scopes.get(scope)
            if not si:
                return  # Unknown scope
            labels = item.get("labels")
            if si.key_labels and labels:
                return  # No labels
            mk = self.get_key(si, item)
            if si.key_fields and not mk[1]:
                return  # No key fields
            if si.key_labels and len(mk[2]) != len(si.key_labels):
                return  # Missed key label
            card = self.get_card(mk)
            if not card:
                return  # Cannot instantiate card
            self.activate_card(card, si, item)

    def load_scopes(self):
        """
        Load ScopeInfo structures
        :return:
        """
        for ms in MetricScope.objects.all():
            self.logger.debug("Loading scope %s", ms.table_name)
            raise NotImplementedError  # @todo: units
            si = ScopeInfo(
                scope=ms.table_name,
                key_fields=tuple(sorted(kf.field_name for kf in ms.key_fields)),
                key_labels=tuple(sorted(kl.label[:-1] for kl in ms.labels if kl.is_required)),
                units=units,
            )
            self.scopes[ms.table_name] = si
            self.logger.debug(
                "[%s] key fields: %s, key labels: %s", si.scope, si.key_fields, si.key_labels
            )

    @staticmethod
    def get_key(si: ScopeInfo, data: Dict[str, Any]) -> MetricKey:
        def iter_key_labels():
            labels = data.get("labels")
            if not labels or not si.key_labels:
                return
            scopes = {f'{l.rsplit("::", 1)[0]}::': l for l in labels}
            for k in si.key_labels:
                v = scopes.get(k)
                if v is not None:
                    yield v

        return (
            si.scope,
            tuple((k, data[k]) for k in si.key_fields if k in data),
            tuple(iter_key_labels()),
        )

    def get_card(self, k: MetricKey) -> Optional[Card]:
        """
        Generate part of computation graph and collect its viable inputs
        :param k: (scope, ((key field, key value), ...), (key label, ...))
        :return:
        """
        card = self.cards.get(k)
        if card:
            return card
        # Generate new CDAG
        cdag = self.get_scope_cdag(k)
        if not cdag:
            return None
        # Apply CDAG to a common graph and collect inputs to the card
        return self.project_cdag(cdag, prefix=str(hash(k)))

    def get_scope_cdag(self, k: MetricKey) -> Optional[CDAG]:
        """
        Generate CDAG for a given metric key
        :param k:
        :return:
        """
        # @todo: Still naive implementation based around the scope
        # @todo: Must be replaced by profile/based card stack generator
        scope = k[0]
        if scope in self.scope_cdag:
            return self.scope_cdag[scope]
        # Not found, create new CDAG
        ms = MetricScope.objects.filter(table_name=k[0]).first()
        if not ms:
            return None  # Not found
        cdag = CDAG(f"scope::{k[0]}", {})
        factory = MetricScopeCDAGFactory(cdag, scope=ms, sticky=True)
        factory.construct()
        self.scope_cdag[k[0]] = cdag
        return cdag

    def project_cdag(self, src: CDAG, prefix: str) -> Card:
        """
        Project `src` to a current graph and return the controlling Card
        :param src:
        :return:
        """

        def unscope(x):
            return x.rsplit("::", 1)[-1]

        nodes: Dict[str, BaseCDAGNode] = {}
        # Clone nodes
        for node_id, node in src.nodes.items():
            nodes[node_id] = node.clone(self.graph, f"{prefix}::{node_id}")
        # Subscribe
        for node_id, o_node in src.nodes.items():
            node = nodes[node_id]
            for r_node, name in o_node.iter_subscribers():
                node.subscribe(nodes[r_node.node_id], name, dynamic=r_node.is_dynamic_input(name))
        # Return resulting cards
        return Card(
            probes={unscope(node.node_id): node for node in nodes.values() if node.name == "probe"},
            senders=tuple(node for node in nodes.values() if node.name == "metrics"),
        )

    def get_state(self) -> Dict[str, Any]:
        """
        Load state for cold start
        :return:
        """
        raise NotImplementedError

    def send_state_wal(self, data: Dict[str, Any]) -> None:
        """
        Send incremental state change
        :param data:
        :return:
        """
        raise NotImplementedError

    def activate_card(self, card: Card, si: ScopeInfo, data: Dict[str, Any]) -> None:
        units = data.get("_units") or {}
        tx = self.graph.begin()
        ts = data["ts"]
        for n in data:
            mu = units.get(n) or si.units.get(n)
            if not units:
                continue  # Missed field
            probe = card.probes.get(n)
            if not probe:
                continue
            probe.activate(tx, "ts", ts)
            probe.activate(tx, "x", data[n])
            probe.activate(tx, "unit", mu)
        # Activate senders
        for sender in card.senders:
            for kf in si.key_fields:
                kv = data.get(kf)
                if kv is not None:
                    sender.activate(tx, kf, kv)
            sender.activate(tx, "ts", ts)
            sender.activate(tx, "labels", data.get("labels") or [])
        # Save state change
        self.send_state_wal(tx.get_changed_state())


if __name__ == "__main__":
    MetricsService().start()
