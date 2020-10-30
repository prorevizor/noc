# ----------------------------------------------------------------------
# NetworkSegmentModel
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional

# NOC modules
from .base import BaseModel
from .typing import Reference
from .networksegmentprofile import NetworkSegmentProfileModel


class NetworkSegmentModel(BaseModel):
    id: str
    parent: Optional[Reference["NetworkSegmentModel"]]
    name: str
    sibling: Optional[str]
    profile: Reference[NetworkSegmentProfileModel]

    _csv_fields = ["id", "parent", "name", "sibling", "profile"]
