# ----------------------------------------------------------------------
# MetricsNode
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional, List
import time

# Third-party modules
from pydantic import BaseModel

# NOC modules
from noc.core.service.loader import get_service
from .base import BaseCDAGNode, ValueType, Category


class MetricsNodeConfig(BaseModel):
    scope: str
    spool: bool = True


NS = 1_000_000_000


class MetricsNode(BaseCDAGNode):
    """
    Collect all dynamic inputs and send all of them as a metric JSON
    """

    name = "metrics"
    categories = [Category.UTIL]
    config_cls = MetricsNodeConfig

    def get_value(self, ts: int, labels: List[str], **kwargs) -> Optional[ValueType]:
        t = time.gmtime(ts / NS)
        r = {
            "date": time.strftime("%Y-%m-%d", t),
            "ts": time.strftime("%Y-%m-%d %H:%M:%S", t),
        }
        if labels:
            r["labels"] = labels
        for n, v in kwargs.items():
            if v is not None:
                r[n] = v
        if self.config.spool:
            get_service().register_metrics(self.config.scope, [r])
        return r
