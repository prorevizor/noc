# ----------------------------------------------------------------------
# AdmDivModel
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional

# NOC modules
from .base import BaseModel
from .typing import Reference


class AdmDivModel(BaseModel):
    id: str
    parent: Optional[Reference["AdmDivModel"]]
    name: str
    short_name: Optional[str]

    _csv_fields = ["id", "parent", "name", "short_name"]
