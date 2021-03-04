# ----------------------------------------------------------------------
# Revoke tokens
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from http import HTTPStatus

# Third-party modules
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

# NOC modules
from ..auth import get_user_from_jwt
from ..models.revoke import RevokeRequest
from ..models.status import StatusResponseError, StatusResponse
from noc.core.service.deps.service import get_service
from noc.services.login.service import LoginService


router = APIRouter()


@router.post("/api/login/revoke", tags=["login"])
async def revoke(req: RevokeRequest, svc: LoginService = Depends(get_service)):
    if req.access_token:
        try:
            get_user_from_jwt(req.access_token, audience="auth")
        except ValueError:
            return StatusResponseError(
                error="unauthorized_client", error_description="Invalid access token"
            )
        if svc.revoke_token(req.access_token) == "exists":
            return JSONResponse(
                content={"error": "invalid_grant", "error_description": "Token is expired"},
                status_code=HTTPStatus.FORBIDDEN,
            )
    if req.refresh_token:
        try:
            get_user_from_jwt(req.refresh_token, audience="auth")
        except ValueError:
            return StatusResponseError(
                error="invalid_request", error_description="Invalid refresh token"
            )
        if svc.revoke_token(req.refresh_token) == "exists":
            return JSONResponse(
                content={"error": "invalid_grant", "error_description": "Token is expired"},
                status_code=HTTPStatus.FORBIDDEN,
            )
    if not req.access_token and not req.refresh_token:
        return StatusResponseError(
            error="invalid_request", error_description="Invalid refresh token"
        )
    return StatusResponse(status=True, message="Ok")
