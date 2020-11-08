# ----------------------------------------------------------------------
# Container loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python Modules
from typing import Optional, Dict, Any
from mongoengine.errors import MultipleObjectsReturned

# NOC modules
from .base import BaseLoader
from ..models.object import Object
from ..models.base import BaseModel
from noc.inv.models.object import Object as ObjectM, ObjectAttr
from noc.inv.models.objectmodel import ObjectModel
from noc.inv.models.objectmodel import ObjectModel as ObjectModelM


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
        "container",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clean_map["model"] = ObjectModel.get_by_name
        self.load_mappings()
        self.managed_object_mappings = self.chain.get_mappings("managedobject")

    def find_object(self, v: Dict[str, Any]) -> Optional[Any]:
        self.logger.debug("Find object: %s", v)
        rs = [d for d in v["data"] if d["interface"] == "remote"]
        if not rs:
            self.logger.warning("Remote interface is not found")
            return None
        rs = rs[0]
        o = self.model.objects.filter(
            data__match={
                "interface": "remote",
                "attr": "id",
                "value": rs["value"],
                "scope": rs["scope"],
            }
        )
        if not o:
            self.logger.debug("Object not found")
            return None
        elif len(o) > 1:
            r = o.filter(name=v["name"])
            if len(r) > 1:
                raise MultipleObjectsReturned
            elif r:
                return list(o)[-1]
        o = list(o)[-1]
        return o

    def clean(self, item: BaseModel) -> Dict[str, Any]:
        r = {k: self.clean_map.get(k, self.clean_any)(v) for k, v in item.dict().items()}
        # Add RemoteSystem Info
        r["data"] += [
            {
                "interface": "remote",
                "attr": "id",
                "value": item.id,
                "scope": str(self.system.remote_system.id),
            }
        ]
        r["data"] = self.clean_data(r["data"])
        # Apply Global Lost&Found if container not set
        if "container" not in r or not r["container"]:

            r["container"] = ObjectM.objects.filter(
                model=ObjectModelM.objects.get(uuid="b0fae773-b214-4edf-be35-3468b53b03f2")
            ).first()
        # @todo Change model method
        return r

    def clean_data(self, data):
        """
        Set ObjectAttr for Object data
        :param data:
        :return:
        """
        r = []
        for d in data:
            if d["interface"] == "management" and d["attr"] == "managed_object":
                if str(d["value"]) in self.managed_object_mappings:
                    d["value"] = int(self.managed_object_mappings[str(d["value"])])
                else:
                    self.logger.warning("Unknown value managedobject")
                    continue
            r += [ObjectAttr(**d)]
        return r

    def purge(self):
        """
        Perform pending deletes
        """
        for r_id, msg in reversed(self.pending_deletes):
            self.logger.debug("Deactivating: %s", msg)
            self.c_delete += 1
            try:
                obj = self.model.objects.get(pk=self.mappings[r_id])
                obj.set_data(interface="remote", attr="deleted", value=True)
                obj.save()
            except self.model.DoesNotExist:
                pass  # Already deleted
        self.pending_deletes = []
