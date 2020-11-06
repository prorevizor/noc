# ----------------------------------------------------------------------
# DivNode
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional

# NOC modules
from .base import BaseCDAGNode, ValueType, Category


class DivNode(BaseCDAGNode):
    """
    Divide `x` by `y`
    """

    name = "div"
    static_inputs = ["x", "y"]
    categories = [Category.OPERATION]

    def get_value(self) -> Optional[ValueType]:
        x, y = self.get_all_inputs()
        if x is None or not y:
            return None
        return x / y
