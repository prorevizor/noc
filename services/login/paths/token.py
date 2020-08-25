# ----------------------------------------------------------------------
# /api/login/token handler
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from fastapi import APIRouter, Request, HTTPException

# NOC modules
from ..models.login import LoginRequest
from ..models.token import TokenResponse
from ..auth import authenticate, get_jwt_token

router = APIRouter()


@router.post("/api/login/token", response_model=TokenResponse, tags=["login", "ext-ui"])
async def token(request: Request, credentials: LoginRequest):
    auth_req = {
        "user": credentials.user,
        "password": credentials.password,
        "ip": request.client.host,
    }
    if authenticate(auth_req):
        return TokenResponse(access_token=get_jwt_token(credentials.user), token_type="bearer")
    raise HTTPException("Access denied", status_code=400)
