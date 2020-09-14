# ----------------------------------------------------------------------
# Liftbridge streams synchronization tool
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Tuple

# NOC modules
from noc.core.management.base import BaseCommand
from noc.core.liftbridge.base import LiftBridgeClient, Metadata
from noc.main.models.pool import Pool
from noc.core.mongo.connection import connect
from noc.core.service.loader import get_dcs
from noc.core.ioloop.util import run_sync


class Command(BaseCommand):
    POOLED_STREAMS = [
        # slot name, stream name
        ("classifier-%s", "events.%s")
    ]

    def handle(self, *args, **options):
        changed = False
        # Get ligtbridge metadata
        meta = self.get_meta()
        rf = min(len(meta.brokers), 2)
        # Apply settings
        for stream, partitions in self.iter_pool_limits():
            self.print("Ensuring stream %s" % stream)
            changed |= self.apply_stream_settings(meta, stream, partitions, rf)
        if changed:
            self.print("CHANGED")
        else:
            self.print("OK")

    def get_meta(self) -> Metadata:
        async def get_meta() -> Metadata:
            async with LiftBridgeClient() as client:
                return await client.fetch_metadata()

        return run_sync(get_meta)

    def iter_pool_limits(self) -> Tuple[str, int]:
        async def get_slot_limits():
            nonlocal slot_name
            return await dcs.get_slot_limit(slot_name)

        dcs = get_dcs()
        connect()
        for pool in Pool.objects.all():
            for slot_mask, stream_mask in self.POOLED_STREAMS:
                slot_name = slot_mask % pool.name
                n_partitions = run_sync(get_slot_limits)
                if n_partitions:
                    yield stream_mask % pool.name, n_partitions

    def apply_stream_settings(self, meta: Metadata, stream: str, partitions: int, rf: int) -> bool:
        def delete_stream(name: str):
            async def wrapper():
                async with LiftBridgeClient() as client:
                    await client.delete_stream(client.get_offset_stream(name))
                    await client.delete_stream(name)

            run_sync(wrapper)

        def create_stream(name: str, n_partitions: int, replication_factor: int):
            async def wrapper():
                async with LiftBridgeClient() as client:
                    await client.create_stream(
                        subject=name,
                        name=name,
                        partitions=n_partitions,
                        replication_factor=replication_factor,
                        init_offsets=True,
                    )

            run_sync(wrapper)

        stream_meta = None
        for m in meta.metadata:
            if m.name == stream:
                stream_meta = m
                break
        # Check if stream is configured properly
        if stream_meta and len(stream_meta.partitions) == partitions:
            return False
        # Check if stream must be dropped
        if stream_meta:
            self.print(
                "Dropping stream %s due to partition/replication factor mismatch (%d -> %d)",
                stream,
                len(stream_meta.partitions),
                partitions,
            )
            delete_stream(stream)
        # Create stream
        self.print("Creating stream %s with %d partitions", stream, partitions)
        create_stream(stream, partitions, rf)
        return True


if __name__ == "__main__":
    Command().run()
