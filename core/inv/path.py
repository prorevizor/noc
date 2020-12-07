# ----------------------------------------------------------------------
# Inventory path finder
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional, Iterable, List, Set, Dict
from dataclasses import dataclass
from enum import Enum

# NOC modules
from noc.inv.models.object import Object
from noc.inv.models.objectconnection import ObjectConnection, ObjectConnectionItem


class ConnAction(Enum, int):
    REJECT = 0
    PASS = 1
    FOUND = 2


@dataclass(frozen=True)
class PathItem(object):
    obj: Object
    connection: str


def find_path(
    obj: Object, connection: str, target_protocols: Iterable[str], max_depth=100
) -> Optional[List[PathItem]]:
    """
    Build shortest path from object's connection until a connection with any of the
    target protocols found.

    :param obj: Object instance
    :param connection: Starting connection name
    :param target_protocols: Iterable of protocols
    :param max_depth: Path Limit
    :return:
    """

    def get_action(item: ObjectConnectionItem) -> ConnAction:
        """
        Check peer connection and return action
        :param item: Object Connection Item
        :return:
        """
        mc = item.object.objects.get_model_connection(item.name)
        if not mc:
            return ConnAction.REJECT
        if not mc.protocols:
            return ConnAction.PASS
        if any(p for p in mc.protocols if p in tp):
            return ConnAction.FOUND
        return ConnAction.REJECT

    def iter_path(final: PathItem, p: PathItem) -> Iterable[PathItem]:
        def iter_reconstruct(pp: PathItem) -> Iterable[PathItem]:
            b = prev.get(pp)
            if b:
                yield from iter_reconstruct(b)
            yield pp

        yield from iter_reconstruct(p)
        yield final

    # Check object connection is exists
    if not obj.has_connection("connection"):
        raise KeyError("Invalid connection name")
    # First connection
    oc = ObjectConnection.objects.filter(
        __raw__={"connection": {"$elemMatch": {"object": obj.id, "name": connection}}}
    ).first()
    if not oc:
        return None
    # Process starting connection
    tp = set(target_protocols)
    wave: Set[Object] = set()  # Search wave
    prev: Dict[PathItem, PathItem] = {}
    p0 = PathItem(obj=obj, connection=connection)
    for c in oc.connection:
        if c.object == obj and c.name == connection:
            continue
        r = get_action(c)
        if r == ConnAction.FOUND:
            # Found
            return [
                p0,
                PathItem(obj=c.object, connection=c),
            ]
        elif r == ConnAction.PASS:
            # Passable
            wave.add(c.object)
            prev[PathItem(obj=c.object, connection=c.connection)] = p0
    if not wave:
        return None  # No suitable completion
    # Process waves
    seen: Set[Object] = set()
    while wave and max_depth > 0:
        new_wave: Set[Object] = set()
        new_seen: Set[Object] = set()
        for oc in ObjectConnection.objects.filter(connection__object__in=list(wave)):
            # Find incoming connection
            incoming: Optional[PathItem] = None
            for c in oc.connection:
                pi = PathItem(obj=c.object, connection=c.connection)
                if pi in prev:
                    incoming = pi
                    break
            if not incoming:
                return None  # Broken path
            # Find path continuations
            for c in oc.connection:
                new_seen.add(c.object)
                if c.object in seen:
                    continue  # Already  tried
                if c.object in wave:
                    # Shortest path cannot include the edge of the wave
                    continue
                pi = PathItem(obj=c.object, connection=c.connection)
                if pi == incoming:
                    continue  # Do not glance back
                r = get_action(c)
                if r == ConnAction.FOUND:
                    # Reconstruct path
                    return list(iter_path(pi, incoming))
                elif r == ConnAction.PASS:
                    new_wave.add(c.object)
                    prev[pi] = incoming
        wave = new_wave
        seen |= new_seen
        max_depth -= 1
    # Wave is stopped, no path
    return None
