# ----------------------------------------------------------------------
# StatusResponse
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional

# Third-party modules
from pydantic import BaseModel


class StatusResponseOk(BaseModel):
    status: bool
    message: Optional[str]


class StatusResponse(BaseModel):
    error: Optional[str] = None
