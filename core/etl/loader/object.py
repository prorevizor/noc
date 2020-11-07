# ----------------------------------------------------------------------
# Container loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python Modules
from typing import Optional, Dict, Any

# NOC modules
from .base import BaseLoader
from ..models.object import Object
from noc.inv.models.object import Object as ObjectM
from noc.inv.models.objectmodel import ObjectModel


class ObjectLoader(BaseLoader):
    """
    Inventory object loader
    """

    name = "object"
    model = ObjectM
    data_model = Object
    fields = [
        "id",
        "name",
        "model",
        "data",
        "parent",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clean_map["model"] = ObjectModel.get_by_name

    def find_object(self, v: Dict[str, Any]) -> Optional[Any]:
        self.logger.debug("Find object: %s", v)
        if not v.get("remote_system") or not v.get("remote_id"):
            self.logger.warning("RS or RID not found")
            return None
        o = self.model.objectsfilter(
            data__match={
                "interface": "remote",
                "attr": "id",
                "value": v["remote_id"],
                "scope": v["remote_system"],
            }
        )
        if len(o) > 1:
            raise Exception("Duplicate object")
        return o
