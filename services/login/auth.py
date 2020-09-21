# ---------------------------------------------------------------------
# Authentication handler
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import logging
from typing import Optional, Dict, Any
import datetime

# Third-party modules
from jose import jwt, jwk
from fastapi.responses import Response

# NOC modules
from noc.config import config
from noc.aaa.models.user import User
from noc.core.perf import metrics
from noc.core.comp import smart_text
from .backends.loader import loader

logger = logging.getLogger(__name__)

# Fields excluded from logging
HIDDEN_FIELDS = {"password", "new_password", "old_password", "retype_password"}

# Build JWK for sign/verify
jwt_key = jwk.construct(config.secret_key, algorithm=config.login.jwt_algorithm).to_dict()


def iter_methods():
    for m in config.login.methods.split(","):
        yield m.strip()


def authenticate(credentials: Dict[str, Any]) -> bool:
    """
    Authenticate user. Returns True when user is authenticated
    """
    c = credentials.copy()
    for f in HIDDEN_FIELDS:
        if f in c:
            c[f] = "***"
    le = "No active auth methods"
    for method in iter_methods():
        bc = loader.get_class(method)
        if not bc:
            logger.error("Cannot initialize backend '%s'", method)
            continue
        backend = bc()
        logger.info("Authenticating credentials %s using method %s", c, method)
        try:
            user = backend.authenticate(**credentials)
            metrics["auth_try", ("method", method)] += 1
        except backend.LoginError as e:
            logger.info("[%s] Login Error: %s", method, smart_text(e))
            metrics["auth_fail", ("method", method)] += 1
            le = smart_text(e)
            continue
        logger.info("Authorized credentials %s as user %s", c, user)
        metrics["auth_success", ("method", method)] += 1
        # Register last login
        if config.login.register_last_login:
            u = User.get_by_username(user)
            if u:
                u.register_login()
        return True
    logger.error("Login failed for %s: %s", c, le)
    return False


def get_jwt_token(user: str, expire: Optional[int] = None, audience: Optional[str] = None) -> str:
    """
    Build JWT token for given user
    :param user: User name
    :param expire: Expiration time in seconds
    :param aud: Token audience
    :return:
    """
    expire = expire or config.login.session_ttl
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire)
    payload = {
        "sub": user,
        "exp": exp,
    }
    if audience:
        payload["aud"] = audience
    return jwt.encode(payload, jwt_key, algorithm=config.login.jwt_algorithm)


def get_user_from_jwt(token: str, audience: Optional[str] = None) -> str:
    """
    Check JWT token and return user.
    Raise ValueError if failed
    :param token:
    :return:
    """
    try:
        token = jwt.decode(token, jwt_key, algorithms=[config.login.jwt_algorithm], audience=audience)
        logger.info("Parsed token: %s", token)
        user = None
        if isinstance(token, dict):
            user = token.get("sub")
            logger.info("Audience: %s", audience)
            if audience and token.get("aud") != audience:
                raise ValueError("Invalid audience")
        if not user:
            raise ValueError("Malformed token")
        return user
    except jwt.ExpiredSignatureError:
        raise ValueError("Expired token")
    except jwt.JWTError as e:
        raise ValueError(str(e))


def set_jwt_cookie(response: Response, user: str) -> None:
    """
    Generate JWT token and append as cookie to response

    :param response:
    :param user:
    :return:
    """
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=config.login.session_ttl)
    response.set_cookie(
        key=config.login.jwt_cookie_name,
        value=get_jwt_token(user, audience="auth"),
        expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    )


def change_credentials(credentials: Dict[str, Any]):
    """
    Change credentials. Return true when credentials changed
    """
    c = credentials.copy()
    for f in HIDDEN_FIELDS:
        if f in c:
            c[f] = "***"
    for method in iter_methods():
        bc = loader.get_class(method)
        if not bc:
            logger.error("Cannot initialize backend '%s'", method)
            continue
        backend = bc()
        logger.info("Changing credentials %s using method %s", c, method)
        try:
            backend.change_credentials(**credentials)
            logger.info("Changed user credentials: %s", c)
            return True
        except NotImplementedError:
            continue
        except backend.LoginError as e:
            logger.error("Failed to change credentials for %s: %s", c, e)
    return False


def revoke_token(token: str) -> None:
    """
    Mark token as revoked. Any futher use will be prohibited
    :param token:
    :return:
    """
    pass  # @todo: Write actual implementation


def is_revoked(token: str) -> bool:
    """
    Check if token is revoked
    :param token: encoded JWT token to check
    :return: True if token is revoked
    """
    return False
