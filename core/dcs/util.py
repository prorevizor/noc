# ----------------------------------------------------------------------
# DCS utilities
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import sys

# Third-party modules
from tornado.ioloop import IOLoop
import tornado.gen

# NOC modules
from noc.core.ioloop.util import run_sync
from noc.core.comp import reraise
from .loader import get_dcs_url, get_dcs_class


def resolve(
    name, hint=None, wait=True, timeout=None, full_result=False, near=False, critical=False
):
    """
    Returns *hint* when service is active or new service
    instance,
    :param name:
    :param hint:
    :param wait:
    :param timeout:
    :param full_result:
    :param near:
    :return:
    """

    @tornado.gen.coroutine
    def _resolve():
        url = get_dcs_url()
        dcs = get_dcs_class()(url)
        try:
            if near:
                r = yield dcs.resolve_near(
                    name,
                    hint=hint,
                    wait=wait,
                    timeout=timeout,
                    full_result=full_result,
                    critical=critical,
                )
            else:
                r = yield dcs.resolve(
                    name,
                    hint=hint,
                    wait=wait,
                    timeout=timeout,
                    full_result=full_result,
                    critical=critical,
                    track=False,
                )
        finally:
            dcs.stop()
        return r

    return run_sync(_resolve)
