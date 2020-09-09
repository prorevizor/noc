# ----------------------------------------------------------------------
# Liftbridge client
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging
from dataclasses import dataclass
import enum
from typing import Optional, Dict, List, AsyncIterable, Tuple
import random
import asyncio
import socket
import struct

# Third-party modules
from grpc.aio import insecure_channel
from grpc import StatusCode
from grpc._cython.cygrpc import EOF

# NOC modules
from noc.config import config
from noc.core.validators import is_ipv4
from .api_pb2_grpc import APIStub
from .api_pb2 import (
    FetchMetadataRequest,
    CreateStreamRequest,
    DeleteStreamRequest,
    PublishRequest,
    SubscribeRequest,
    AckPolicy as _AckPolicy,
    StartPosition as _StartPosition,
)
from .error import rpc_error, ErrorNotFound, ErrorChannelClosed, ErrorUnavailable
from .message import Message

logger = logging.getLogger(__name__)


class AckPolicy(enum.IntEnum):
    LEADER = _AckPolicy.LEADER
    ALL = _AckPolicy.ALL
    NONE = _AckPolicy.NONE


class StartPosition(enum.IntEnum):
    NEW_ONLY = _StartPosition.NEW_ONLY  # Start at new messages after the latest
    OFFSET = _StartPosition.OFFSET  # Start at a specified offset
    EARLIEST = _StartPosition.EARLIEST  # Start at the oldest message
    LATEST = _StartPosition.LATEST  # Start at the newest message
    TIMESTAMP = _StartPosition.TIMESTAMP  # Start at a specified timestamp
    RESUME = 9999  # Non-standard -- resume from next to last processed


@dataclass
class Broker(object):
    id: str
    host: str
    port: int


@dataclass
class PartitionMetadata(object):
    id: int
    leader: str
    replicas: List[str]
    isr: List[str]
    high_watermark: int
    newest_offset: int


@dataclass
class StreamMetadata(object):
    name: str
    subject: str
    partitions: Dict[int, PartitionMetadata]


@dataclass
class Metadata(object):
    brokers: List[Broker]
    metadata: List[StreamMetadata]


class LiftBridgeClient(object):
    _offset_struct = struct.Struct("!Q")
    _offset_key = b"1"

    # @todo: Resilient RPC
    # @todo: Dedicated sub channel
    def __init__(self):
        self.channel = None
        self.stub = None

    async def __aenter__(self) -> "LiftBridgeClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @staticmethod
    def get_offset_stream(stream: str) -> str:
        """
        Returns name for offset stream
        :param stream:
        :return:
        """
        return "__offset.%s" % stream

    @classmethod
    def encode_offset(cls, value: int) -> bytes:
        """
        Encode offset value to bytes stream
        :param value:
        :return:
        """
        return cls._offset_struct.pack(value)

    @classmethod
    def decode_offset(cls, value: bytes) -> int:
        """
        Encode offset value to bytes stream
        :param value:
        :return:
        """
        return cls._offset_struct.unpack(value)[0]

    async def connect(self) -> None:
        svc = random.choice(config.liftbridge.addresses)
        logger.debug("Connecting %s:%s", svc.host, svc.port)
        self.channel = insecure_channel("%s:%s" % (svc.host, svc.port))
        await self.channel.channel_ready()
        self.stub = APIStub(self.channel)

    async def close(self) -> None:
        logger.debug("Closing channel")
        await self.channel.close()
        self.channel = None
        self.stub = None

    async def reconnect(self) -> None:
        await self.close()
        await self.connect()

    async def fetch_metadata(self) -> Metadata:
        r = await self.stub.FetchMetadata(FetchMetadataRequest())
        return Metadata(
            brokers=[Broker(id=b.id, host=b.host, port=b.port) for b in r.brokers],
            metadata=[
                StreamMetadata(
                    name=m.name,
                    subject=m.subject,
                    partitions={
                        p.id: PartitionMetadata(
                            id=p.id,
                            leader=p.leader,
                            replicas=list(p.replicas),
                            isr=list(p.isr),
                            high_watermark=p.highWatermark,
                            newest_offset=p.newestOffset,
                        )
                        for p in m.partitions.values()
                    },
                )
                for m in r.metadata
            ],
        )

    async def create_stream(
        self,
        subject: str,
        name: str,
        group: Optional[str] = None,
        replication_factor: int = 1,
        partitions: int = 1,
        enable_compact: bool = False,
        init_offsets: bool = False,
    ):
        with rpc_error():
            req = CreateStreamRequest(
                subject=subject,
                name=name,
                group=group,
                replicationFactor=replication_factor,
                partitions=partitions,
            )
            if enable_compact:
                req.CompactEnabled.value = True
            await self.stub.CreateStream(req)
            if init_offsets:
                # Create additional stream to store offsets
                await self.create_stream(
                    subject=self.get_offset_stream(subject),
                    name=self.get_offset_stream(name),
                    replication_factor=replication_factor,
                    partitions=partitions,
                    enable_compact=True,
                )
                # Initialize with starting offset
                for i in range(partitions):
                    await self.commit_offset(stream=name, partition=i, offset=-1)

    async def delete_stream(self, name: str) -> None:
        with rpc_error():
            await self.stub.DeleteStream(DeleteStreamRequest(name=name))

    async def publish(
        self,
        value: bytes,
        stream: Optional[str] = None,
        key: Optional[bytes] = None,
        partition: Optional[int] = None,
        headers: Optional[Dict[str, bytes]] = None,
        ack_inbox: Optional[str] = None,
        correlation_id: Optional[str] = None,
        ack_policy: AckPolicy = AckPolicy.LEADER,
    ) -> None:
        # Build message
        req = PublishRequest(value=value, ackPolicy=ack_policy.value)
        if stream:
            req.stream = stream
        if key:
            req.key = key
        if partition:
            req.partition = partition
        if headers:
            req.headers = headers
        if ack_inbox:
            req.ackInbox = ack_inbox
        if correlation_id:
            req.correlationIid = correlation_id
        # Publish
        while True:
            try:
                with rpc_error():
                    await self.stub.Publish(req)
                    break
            except ErrorUnavailable:
                logger.info("Loosing connection to current cluster member. Trying to reconnect")
                await asyncio.sleep(1)
                await self.reconnect()

    async def subscribe(
        self,
        stream: str,
        partition: Optional[int] = None,
        start_position: StartPosition = StartPosition.NEW_ONLY,
        start_offset: Optional[int] = None,
        start_timestamp: Optional[int] = None,
        resume: bool = False,
        timeout: Optional[int] = None,
        allow_isr: bool = False,
    ) -> AsyncIterable[Message]:
        # Build request
        req = SubscribeRequest(stream=stream)
        to_restore_position = False
        if partition:
            req.partition = partition
        if resume:
            req.resume = resume
        if allow_isr:
            req.readISRReplica = True
        if start_offset is not None:
            req.startPosition = StartPosition.OFFSET
            req.startOffset = start_offset
        elif start_timestamp is not None:
            req.startPosition = StartPosition.TIMESTAMP
            req.startTimestamp = start_timestamp
        elif start_position == StartPosition.RESUME:
            logger.debug("Getting stored offset for stream '%s'" % stream)
            req.startPosition = StartPosition.OFFSET
            to_restore_position = True
            logger.debug("Resuming from offset %d", req.startOffset)
        else:
            req.startPosition = start_position
        while True:
            try:
                async for msg in self._subscribe(req, restore_position=to_restore_position):
                    yield msg
            except ErrorUnavailable:
                logger.error("Subscriber looses connection to partition node. Trying to reconnect")
                await asyncio.sleep(1)

    async def _subscribe(
        self, req: SubscribeRequest, restore_position: bool = False
    ) -> AsyncIterable[Message]:
        with rpc_error():
            logging.debug("[%s:%s] Resolving partition node", req.stream, req.partition)
            host, port = await self.resolve_subscription_source(
                req.stream, partition=req.partition, allow_isr=bool(req.readISRReplica)
            )
            logger.debug("Connecting %s:%s", host, port)
            # Open separate channel for subscription
            async with insecure_channel("%s:%s" % (host, port)) as channel:
                await channel.channel_ready()
                logger.debug("Subscribing stream '%s'", req.stream)
                stub = APIStub(channel)
                if restore_position:
                    req.startOffset = await self.get_stored_offset(
                        req.stream, partition=req.partition
                    )
                call = stub.Subscribe(req)
                # NB: We cannot use `async for msg in call` construction
                # Due to liftbridge protocol specific:
                # --- CUT ---
                # When the subscription stream is created, the server sends an empty message
                # to indicate the subscription was successfully created. Otherwise, an error
                # is sent on the stream if the subscribe failed. This handshake message
                # must be handled and should not be exposed to the user.
                # --- CUT ---
                # So grpc aio implementation treats first message as aio.EOF
                # and hangs forever trying to get error status from core.
                # So we use own inlined `_fetch_stream_responses` implementation here
                msg = await call._read()
                # Should be EOF, error otherwise
                if msg is not EOF:
                    raise ErrorChannelClosed()
                # Next, process all other messages
                msg = await call._read()
                while msg:
                    yield Message(
                        value=msg.value,
                        subject=msg.subject,
                        offset=msg.offset,
                        timestamp=msg.timestamp,
                        key=msg.key,
                        partition=msg.partition,
                    )
                    msg = await call._read()
                # Get core message to explain the result
                code = await call.code()
                if code is StatusCode.UNAVAILABLE:
                    raise ErrorUnavailable()
                raise ErrorChannelClosed(str(code))

    async def resolve_subscription_source(
        self, stream: str, partition: Optional[int] = None, allow_isr: bool = False
    ) -> Tuple[str, int]:
        """
        Returns (host, port) of active node to be subscribed to.
        Connect to partition leader when `allow_isr` is False,
        or to random partition node, when True.

        :param stream: Stream name
        :param partition: Partition number
        :param allow_isr: True, if allowed to connect to random node
        :return: (host, port)
        """

        async def _resolve_broker(b_id: str) -> Tuple[str, int]:
            logger.debug("Resolving broker %s", b_id)
            for broker in meta.brokers:
                if broker.id != b_id:
                    continue
                if not is_ipv4(broker.host):
                    # Resolve hostname
                    try:
                        addr_info = await asyncio.get_running_loop().getaddrinfo(
                            broker.host, None, proto=socket.IPPROTO_TCP
                        )
                        addrs = [x[4][0] for x in addr_info if x[0] == socket.AF_INET]
                        return random.choice(addrs), broker.port
                    except socket.gaierror:
                        raise ErrorNotFound("Cannot resolve broker address '%s'" % broker.host)

                return broker.host, broker.port
            raise ErrorNotFound("Broker not found")

        # Request cluster topology
        while True:
            meta = await self.fetch_metadata()
            if not meta.metadata:
                # No streams, election in progress, wait for a while
                logger.info("Waiting for election")
                await asyncio.sleep(1)
                continue
            s_data = [m for m in meta.metadata if m.name == stream]
            if not s_data:
                raise ErrorNotFound("Stream not found")
            break
        p_data = s_data[0].partitions.get(partition or 0)
        if not p_data:
            raise ErrorNotFound("Partition not found")
        if allow_isr:
            return await _resolve_broker(random.choice(p_data.isr))
        return await _resolve_broker(p_data.leader)

    async def commit_offset(self, stream: str, partition: int, offset: int) -> None:
        """
        Store last processed position of the stream
        :param stream:
        :param partition:
        :param offset:
        :return:
        """
        logger.debug("[%s:%s] Committing offset %d", stream, partition, offset)
        await self.publish(
            stream=self.get_offset_stream(stream),
            value=self.encode_offset(offset + 1),
            partition=partition,
            key=self._offset_key,
        )

    async def get_stored_offset(self, stream: str, partition: int) -> int:
        """
        Fetch stored offset for the stream
        :param stream:
        :param partition:
        :return:
        """
        async for msg in self.subscribe(
            self.get_offset_stream(stream), partition=partition, start_position=StartPosition.LATEST
        ):
            return self.decode_offset(msg.value)
