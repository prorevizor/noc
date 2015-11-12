# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## SNMP methods implementation
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import logging
import socket
import errno
## Third-party modules
from tornado.gen import coroutine, Return
## NOC modules
from noc.core.snmp.version import SNMP_v2c
from noc.core.snmp.get import (get_pdu, getnext_pdu, getbulk_pdu,
                               parse_get_response)
from noc.core.snmp.set import set_pdu
from noc.core.snmp.error import (NO_ERROR, NO_SUCH_NAME,
                                 SNMPError, TIMED_OUT)
from noc.core.ioloop.udp import UDPSocket

_ERRNO_WOULDBLOCK = (errno.EWOULDBLOCK, errno.EAGAIN)
logger = logging.getLogger(__name__)
BULK_MAX_REPETITIONS = 20


@coroutine
def snmp_get(address, oids, port=161,
             community="public",
             version=SNMP_v2c,
             timeout=10,
             tos=None,
             ioloop=None):
    """
    Perform SNMP get request and returns Future to be used
    inside @tornado.gen.coroutine
    """
    oid_map = {}
    if isinstance(oids, basestring):
        oids = [oids]
    elif isinstance(oids, dict):
        oid_map = dict((oids[k], k) for k in oids)
        oids = oids.values()
    else:
        raise ValueError("oids must be either string or dict")
    logger.debug("[%s] SNMP GET %s", address, oids)
    # Send GET PDU
    pdu = get_pdu(community=community, oids=oids)
    sock = UDPSocket(ioloop=ioloop, tos=tos)
    sock.settimeout(timeout)
    # Wait for result
    try:
        yield sock.sendto(pdu, (address, port))
        data, addr = yield sock.recvfrom(4096)
    except socket.timeout:
        raise SNMPError(code=TIMED_OUT, oid=oids[0])
    finally:
        sock.close()
    resp = parse_get_response(data)
    if resp.error_status != NO_ERROR:
        oid = None
        if resp.error_index and resp.varbinds:
            oid = resp.varbinds[resp.error_index - 1][0]
        logger.debug("[%s] SNMP error: %s %s",
                     address, oid, resp.error_status)
        raise SNMPError(code=resp.error_status, oid=oid)
    else:
        # Success
        if oid_map:
            result = {}
            for k, v in resp.varbinds:
                if k in oid_map:
                    result[oid_map[k]] = v
        else:
            result = resp.varbinds[0][1]
        logger.debug("[%s] GET result: %s", address, result)
        raise Return(result)


@coroutine
def snmp_count(address, oid, port=161,
               community="public",
               version=SNMP_v2c,
               timeout=10,
               bulk=False,
               filter=None,
               max_repetitions=BULK_MAX_REPETITIONS,
               tos=None,
               ioloop=None):
    """
    Perform SNMP get request and returns Future to be used
    inside @tornado.gen.coroutine
    """
    logger.debug("[%s] SNMP COUNT %s", address, oid)
    if not filter:
        filter = lambda x, y: True
    poid = oid + "."
    result = 0
    sock = UDPSocket(ioloop=ioloop, tos=tos)
    sock.settimeout(timeout)
    while True:
        # Get PDU
        if bulk:
            pdu = getbulk_pdu(community, oid,
                              max_repetitions=max_repetitions)
        else:
            pdu = getnext_pdu(community, oid)
        # Send request and wait for response
        try:
            yield sock.sendto(pdu, (address, port))
            data, addr = yield sock.recvfrom(4096)
        except socket.timeout:
            sock.close()
            raise SNMPError(code=TIMED_OUT, oid=oid)
        # Parse response
        resp = parse_get_response(data)
        if resp.error_status == NO_SUCH_NAME:
            # NULL result
            break
        elif resp.error_status != NO_ERROR:
            # Error
            sock.close()
            raise SNMPError(code=resp.error_status, oid=oid)
        else:
            # Success value
            for oid, v in resp.varbinds:
                if oid.startswith(poid):
                    # Next value
                    if filter(oid, v):
                        result += 1
                else:
                    logger.debug("[%s] COUNT result: %s",
                                 address, result)
                    sock.close()
                    raise Return(result)
    sock.close()


@coroutine
def snmp_getnext(address, oid, port=161,
                 community="public",
                 version=SNMP_v2c,
                 timeout=10,
                 bulk=False,
                 filter=None,
                 max_repetitions=BULK_MAX_REPETITIONS,
                 only_first=False,
                 tos=None,
                 ioloop=None):
    """
    Perform SNMP GETNEXT/BULK request and returns Future to be used
    inside @tornado.gen.coroutine
    """
    logger.debug("[%s] SNMP GETNEXT %s", address, oid)
    if not filter:
        filter = lambda x, y: True
    poid = oid + "."
    result = []
    sock = UDPSocket(ioloop=ioloop, tos=tos)
    sock.settimeout(timeout)
    while True:
        # Get PDU
        if bulk:
            pdu = getbulk_pdu(community, oid,
                              max_repetitions=max_repetitions)
        else:
            pdu = getnext_pdu(community, oid)
        # Send request and wait for response
        try:
            yield sock.sendto(pdu, (address, port))
            data, addr = yield sock.recvfrom(4096)
        except socket.timeout:
            sock.close()
            raise SNMPError(code=TIMED_OUT, oid=oid)
        # Parse response
        resp = parse_get_response(data)
        if resp.error_status == NO_SUCH_NAME:
            # NULL result
            break
        elif resp.error_status != NO_ERROR:
            # Error
            sock.close()
            raise SNMPError(code=resp.error_status, oid=oid)
        else:
            # Success value
            for oid, v in resp.varbinds:
                if oid.startswith(poid) and not (only_first and result):
                    # Next value
                    if filter(oid, v):
                        result += [(oid, v)]
                else:
                    logger.debug("[%s] GETNEXT result: %s",
                                 address, result)
                    sock.close()
                    raise Return(result)
    sock.close()

@coroutine
def snmp_set(address, varbinds, port=161,
             community="public",
             version=SNMP_v2c,
             timeout=10,
             tos=None,
             ioloop=None):
    """
    Perform SNMP set request and returns Future to be used
    inside @tornado.gen.coroutine
    """
    logger.debug("[%s] SNMP SET %s", address, varbinds)
    sock = UDPSocket(ioloop=ioloop, tos=tos)
    sock.settimeout(timeout)
    # Send GET PDU
    pdu = set_pdu(community=community, varbinds=varbinds)
    # Wait for result
    try:
        yield sock.sendto(pdu, (address, port))
        data, addr = yield sock.recvfrom(4096)
    except socket.timeout:
        raise SNMPError(code=TIMED_OUT, oid=varbinds[0][0])
    resp = parse_get_response(data)
    if resp.error_status != NO_ERROR:
        oid = None
        if resp.error_index and resp.varbinds:
            oid = resp.varbinds[resp.error_index - 1][0]
        logger.debug("[%s] SNMP error: %s %s",
                     address, oid, resp.error_status)
        sock.close()
        raise SNMPError(code=resp.error_status, oid=oid)
    else:
        logger.debug("[%s] SET result: OK", address)
        sock.close()
        raise Return(True)
