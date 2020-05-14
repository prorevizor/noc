# ----------------------------------------------------------------------
# Telnet CLI
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging
import codecs

# Third-party modules
from tornado.iostream import IOStream
from typing import List, Optional, Union
from tornado.concurrent import Future

# NOC modules
from noc.core.perf import metrics
from .base import CLI

_logger = logging.getLogger(__name__)


IAC = 0xFF  # Interpret As Command
DONT = 0xFE
DO = 0xFD
WONT = 0xFC
WILL = 0xFB
SB = 0xFA
SE = 0xF0
NAWS = 0x1F
AO = 0xF5
AYT = 0xF6

B_IAC = b"\xFF"
B_SB = b"\xFA"
B_SE = b"\xF0"
B_IAC2 = B_IAC + B_IAC
B_IAC_SB = B_IAC + B_SB
B_IAC_SE = B_IAC + B_SE
B_NAWS = b"\x1F"

B_OPT_TTYPE_IS = b"\x18\x00"
B_OPT_WS = b"\x1f"

B_TERMINAL_TYPE = b"XTERM"

IAC_CMD = {DO: "DO", DONT: "DONT", WILL: "WILL", WONT: "WONT"}

IGNORED_CMD = {AO, AYT}

TELNET_OPTIONS = {
    0: "BINARY",
    1: "ECHO",
    2: "RCP",
    3: "SGA",
    4: "NAMS",
    5: "STATUS",
    6: "TM",
    7: "RCTE",
    8: "NAOL",
    9: "NAOP",
    10: "NAOCRD",
    11: "NAOHTS",
    12: "NAOHTD",
    13: "NAOFFD",
    14: "NAOVTS",
    15: "NAOVTD",
    16: "NAOLFD",
    17: "XASCII",
    18: "LOGOUT",
    19: "BM",
    20: "DET",
    21: "SUPDUP",
    22: "SUPDUPOUTPUT",
    23: "SNDLOC",
    24: "TTYPE",
    25: "EOR",
    26: "TUID",
    27: "OUTMRK",
    28: "TTYLOC",
    29: "3270REGIME",
    30: "X3PAD",
    31: "NAWS",
    32: "TSPEED",
    33: "LFLOW",
    34: "LINEMODE",
    35: "XDISPLOC",
    36: "OLD_ENVIRON",
    37: "AUTHENTICATION",
    38: "ENCRYPT",
    39: "NEW_ENVIRON",
    40: "TN3270E",
    41: "XAUTH",
    42: "CHARSET",
    45: "SLE",
    255: "EXOPL",
}

# ECHO+SGA+TTYPE+NAWS
ACCEPTED_TELNET_OPTIONS = {0x01, 0x03, 0x18, 0x1F}

OPTS = {B_OPT_TTYPE_IS: "TTYPE IS", B_OPT_WS: "WS"}


def bytes_seq(*args: int) -> bytes:
    return bytes(args)


class TelnetParser(object):
    """
    Telnet protocol state and commands processing
    """

    def __init__(self, logger=None, writer=None, naws=b"\x00\x80\x00\x80"):
        self.logger = logger or _logger
        self.writer = writer
        self.iac_seq: bytes = b""
        self.out_iac_seq: List[bytes] = []
        self.naws = naws

    def feed(self, chunk: bytes) -> bytes:
        """
        Feed chunk of data to parser

        :param chunk: String
        :return: Parsed data
        """
        if self.iac_seq and chunk:
            # Restore incomplete IAC context
            chunk = self.iac_seq + chunk
            self.iac_seq = b""
        r: List[bytes] = []
        while chunk:
            left, seq, right = chunk.partition(B_IAC)
            # Pass clear part
            r += [left]
            # Process control sequences
            if seq:
                # Process IAC sequence
                if not right or len(right) == 1:
                    # Incomplete sequence
                    # Collect for next round
                    self.iac_seq = B_IAC + right
                    break
                ctl = right[0]
                if ctl == IAC:
                    # <IAC> <IAC> leads to single <IAC>
                    r += [B_IAC]
                    chunk = right[1:]
                elif ctl in IGNORED_CMD:
                    # Ignore command
                    chunk = right[1:]
                elif ctl != SB:
                    # Process IAC <cmd> <opt>
                    self.process_iac(ctl, right[1])
                    chunk = right[2:]
                else:
                    # Process IAC SB ... SE sequence
                    # @todo: Use .partition()
                    if B_SE not in right:
                        self.iac_seq = B_IAC + right
                        break
                    i = right.index(B_SE)
                    self.process_iac_sb(right[1 : i - 1])
                    chunk = right[i + 1 :]
            else:
                # Return leftovers
                break
        if self.out_iac_seq:
            out_seq = b"".join(self.out_iac_seq)
            self.writer(out_seq)
            self.out_iac_seq = []
        return b"".join(r)

    def send_iac(self, cmd: int, opt: int) -> None:
        """
        Send IAC response
        """
        self.logger.debug("Send %s", self.iac_repr(cmd, opt))
        self.out_iac_seq += [bytes_seq(IAC, cmd, opt)]

    def send_iac_sb(self, opt: bytes, data: Optional[bytes] = None) -> None:
        sb: List[bytes] = [B_IAC_SB, opt]
        if data:
            sb += [data]
        sb += [B_IAC_SE]
        s_opt = OPTS.get(opt)
        if not s_opt:
            s_opt = "%r" % opt
        self.logger.debug("Send IAC SB %s %r IAC SE", s_opt, data)
        self.out_iac_seq += sb

    def process_iac(self, cmd: int, opt: int) -> None:
        """
        Process IAC command.
        """
        self.logger.debug("Received %s", self.iac_repr(cmd, opt))
        if cmd == DO:
            r = WILL if opt in ACCEPTED_TELNET_OPTIONS else WONT
        elif cmd == DONT:
            r = WONT
        elif cmd == WILL:
            r = DO if opt in ACCEPTED_TELNET_OPTIONS else DONT
        elif cmd == WONT:
            r = DONT
        else:
            return  # Ignore invalid IAC command
        self.send_iac(r, opt)
        # Send NAWS response
        if cmd == DO and opt == NAWS:
            self.send_iac_sb(B_NAWS, self.naws)

    def process_iac_sb(self, sb: bytes) -> None:
        if sb == b"\x18\x01":
            self.logger.debug("Received IAC SB TTYPE SEND IAC SE")
            self.send_iac_sb(b"\x18\x00", B_TERMINAL_TYPE)
        else:
            self.logger.debug("Received IAC SB %s IAC SE", codecs.encode(sb, "hex"))

    @staticmethod
    def iac_repr(cmd: int, opt: int) -> str:
        """
        Human-readable IAC sequence
        :param cmd:
        :param opt:
        :return:
        """
        return "%s %s" % (IAC_CMD.get(cmd, cmd), TELNET_OPTIONS.get(opt, opt))

    @staticmethod
    def escape(data: bytes) -> bytes:
        return data.replace(B_IAC, B_IAC2)

    def set_writer(self, writer):
        """
        Replace current writer.

        :param writer: Callable accepting bytes
        :return:
        """
        self.writer = writer


class TelnetIOStream(IOStream):
    def __init__(self, sock, cli, *args, **kwargs):
        super().__init__(sock, *args, **kwargs)
        self.cli = cli
        self.logger = cli.logger
        self.parser = TelnetParser(
            logger=self.logger, writer=self.write_to_fd, naws=cli.profile.get_telnet_naws()
        )

    async def startup(self):
        if self.cli.profile.telnet_send_on_connect:
            self.logger.debug("Sending %r on connect", self.cli.profile.telnet_send_on_connect)
            await self.write(self.cli.profile.telnet_send_on_connect)

    def read_from_fd(self, buf: Union[bytearray, memoryview]) -> Optional[int]:
        metrics["telnet_reads"] += 1
        n = super().read_from_fd(buf)
        if n == 0:
            return 0  # EOF
        if n is None:
            metrics["telnet_reads_blocked"] += 1
            return None  # EAGAIN
        metrics["telnet_read_bytes"] += n
        parsed = self.parser.feed(buf[:n])
        pn = len(parsed)
        if not pn:
            return None  # Incomplete data, blocked until next read
        buf[:pn] = parsed
        return pn

    def write(self, data: Union[bytes, memoryview]) -> "Future[None]":
        data = self.parser.escape(data)
        metrics["telnet_writes"] += 1
        metrics["telnet_write_bytes"] += len(data)
        return super().write(data)


class TelnetCLI(CLI):
    name = "telnet"
    default_port = 23
    iostream_class = TelnetIOStream
