# ----------------------------------------------------------------------
# ProbeNode
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional

# Third-party modules
from pydantic import BaseModel

# NOC modules
from .base import BaseCDAGNode, ValueType, Category

MAX31 = 0x7FFFFFFF
MAX32 = 0xFFFFFFFF
MAX64 = 0xFFFFFFFFFFFFFFFF
NS = 1_000_000_000


class ProbeNodeState(BaseModel):
    lt: Optional[int] = None
    lv: Optional[ValueType] = None


class ProbeNodeConfig(BaseModel):
    unit: str


class ProbeNode(BaseCDAGNode):
    """
    Entrance for collected metrics. Accepts timestamp, value and measurement units.
    Converts counter when necessary
    """

    name = "probe"
    config_cls = ProbeNodeConfig
    state_cls = ProbeNodeState
    categories = [Category.UTIL]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.convert = MS_CONVERT[self.config.unit]

    def get_value(self, x: ValueType, ts: int, unit: str) -> Optional[ValueType]:
        # No translation
        if unit == self.config.unit:
            return x
        # Plain conversion
        expr, counter_scale = self.convert[unit.lower()]
        if counter_scale is not None:
            # Counter
            return self.from_counter(x, ts, counter_scale)
        else:
            # Plain conversion
            self.reset_state()
            return expr(x)

    def reset_state(self):
        self.state.lt = None
        self.state.lv = None

    @staticmethod
    def get_bound(v: int) -> int:
        """
        Detect wrap bound
        :param v:
        :return:
        """
        if v <= MAX31:
            return MAX31
        if v <= MAX32:
            return MAX32
        return MAX64

    def from_delta(self, value: ValueType, ts: int, scale: int) -> Optional[ValueType]:
        """
        Calculate value from delta, gently handling overflows
        :param value:
        :param ts:
        :param scale:
        """
        if self.state.lt is None:
            # Empty state, update and skip round
            self.state.lt = ts
            self.state.lv = value
            return None
        if ts <= self.state.lt:
            self.reset_state()
            return None  # Time stepback
        dv = value - self.state.lv
        if dv >= 0:
            self.state.lt = ts
            self.state.lv = value
            return scale * dv
        # Counter wrapped, either due to wrap or due to stepback
        bound = self.get_bound(self.state.lv)
        # Wrap distance
        d_wrap = value + (bound - self.state.lv)
        if -dv < d_wrap:
            # Possible counter stepback, skip value
            self.reset_state()
            return None
        # Counter wrap
        self.state.lt = ts
        self.state.lv = value
        return d_wrap * scale

    def from_counter(self, value: ValueType, ts: int, scale: int) -> Optional[ValueType]:
        if self.state.lt is None:
            # Empty state, update and skip round
            self.state.lt = ts
            self.state.lv = value
            return None
        dt = ts - self.state.lt
        v = self.from_delta(value, ts, scale)
        if v is None:
            return v
        return v * NS / dt


MS_CONVERT = {
    # Name -> alias -> (expr, scale)
    # expr for plain conversion, scale for counters
    "bit": {"byte": (lambda x: x * 8, None)},
    "bit/s": {"byte/s": (lambda x: x * 8, None), "bit": (None, 1), "byte": (None, 8)},
}
