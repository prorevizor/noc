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
        raise NotImplementedError

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
