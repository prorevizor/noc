# ----------------------------------------------------------------------
# Various IOLoop utilities
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import sys
import asyncio
import logging

# Third-party modules
from typing import Callable, TypeVar, List, Tuple, Any

# NOC modules
from noc.config import config
from noc.core.comp import reraise

logger = logging.getLogger(__name__)
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
    if prev_loop:
        asyncio._set_running_loop(prev_loop)
    else:
        asyncio._set_running_loop(None)
        asyncio.get_event_loop_policy()._local._set_called = False
    # @todo: close_all
    if error:
        reraise(*error[0])
    return result[0]


_setup_completed = False


def setup_asyncio() -> None:
    """
    Initial setup of asyncio

    :return:
    """
    global _setup_completed

    if _setup_completed:
        return
    logger.info("Setting up asyncio event loop policy")
    if config.features.use_uvlib:
        try:
            import uvloop

            logger.info("Setting up libuv event loop")
            uvloop.install()
        except ImportError:
            logger.info("libuv is not installed, using default event loop")
    asyncio.set_event_loop_policy(NOCEventLoopPolicy())
    _setup_completed = True


class NOCEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    def get_event_loop(self) -> asyncio.AbstractEventLoop:
        try:
            return super().get_event_loop()
        except RuntimeError:
            loop = self.new_event_loop()
            self.set_event_loop(loop)
            return loop
