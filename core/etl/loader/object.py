# ----------------------------------------------------------------------
# Container loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

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
        "container",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clean_map["model"] = ObjectModel.get_by_name
