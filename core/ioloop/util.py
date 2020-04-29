# ----------------------------------------------------------------------
# Various IOLoop utilities
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import sys
import asyncio

# Third-party modules
from typing import Callable, TypeVar, List, Tuple, Any
from tornado.ioloop import IOLoop
import tornado.gen

# NOC modules
from noc.core.comp import reraise

T = TypeVar("T")


def run_sync(cb: Callable[..., T], close_all: bool = True) -> T:
    """
    Run callable on dedicated IOLoop in safe manner
    and return result or raise error

    :param cb: Callable to be runned on IOLoop
    :param close_all: Close all file descriptors
    :return: Callable result
    """

    async def wrapper():
        try:
            r = await cb()
            result.append(r)
        except Exception:
            error.append(sys.exc_info())

    result: List[T] = []
    error: List[Tuple[Any, Any, Any]] = []

    prev_loop = asyncio._get_running_loop()
    new_loop = asyncio.new_event_loop()
    if prev_loop:
        # Reset running loop
        asyncio._set_running_loop(None)
    new_loop.run_until_complete(wrapper())
    asyncio._set_running_loop(prev_loop)
    # @todo: close_all
    if error:
        reraise(*error[0])
    return result[0]
