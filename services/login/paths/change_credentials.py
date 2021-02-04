# ----------------------------------------------------------------------
# /api/login/change_credentials handler
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from fastapi import APIRouter

# NOC modules
from ..auth import change_credentials as _change_credentials
from ..models.changecredentials import ChangeCredentialsRequest
from ..models.status import StatusResponseOk

router = APIRouter()


@router.put(
    "/api/login/change_credentials", response_model=StatusResponseOk, tags=["login", "ext-ui"]
)
async def change_credentials(req: ChangeCredentialsRequest):
    creds = {
        "user": req.user,
        "old_password": req.old_password,
        "new_password": req.new_password,
    }
    if _change_credentials(creds):
        return StatusResponseOk(status=True)
    return StatusResponseOk(status=False, message="Failed to change credentials")
