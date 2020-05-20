# ----------------------------------------------------------------------
# Tornado IOLoop UDP socket
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import socket
from typing import Tuple, Optional, Callable
import asyncio


class UDPSocket(object):
    """
    UDP socket abstraction

    async def test():
        sock = UDPSocket()
        # Send request
        await sock.sendto(data, (address, port))
        # Wait reply
        data, addr = await sock.recvfrom(4096)
        # Close socket
        sock.close()
    """

    def __init__(self, tos: Optional[int] = None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if tos:
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, tos)
        self.socket.setblocking(False)

    def __del__(self):
        self.close()

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    async def send_and_receive(
        self, data: bytes, address: Tuple[str, int]
    ) -> Tuple[bytes, Tuple[str, int]]:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        await loop.create_datagram_endpoint(_get_protocol(data, address, future), sock=self.socket)
        return await future


class UDPSendRecvProtocol(asyncio.DatagramProtocol):
    def __init__(self, data: bytes, addr: Tuple[str, int], future: asyncio.Future):
        self.data = data
        self.addr = addr
        self.future = future
        self.transport: Optional[asyncio.BaseTransport] = None

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport
        self.transport.sendto(self.data, self.addr)

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        self.future.set_result((data, addr))
        if self.transport:
            self.transport.close()
            self.transport = None

    def error_received(self, exc: Exception) -> None:
        self.future.set_exception(exc)
        if self.transport:
            self.transport.close()
            self.transport = None


def _get_protocol(
    data: bytes, address: Tuple[str, int], future: asyncio.Future
) -> Callable[[], asyncio.BaseProtocol]:
    def wrap():
        return UDPSendRecvProtocol(data, address, future)

    return wrap


class UDPSocketContext(object):
    def __init__(self, sock: Optional[UDPSocket] = None, tos: Optional[int] = None):
        if sock:
            self.sock = sock
            self.to_close = False
        else:
            self.sock = UDPSocket(tos=tos)
            self.to_close = True

    def __enter__(self):
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.to_close:
            self.sock.close()
            self.sock = None
