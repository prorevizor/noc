#!./bin/python
# ---------------------------------------------------------------------
# Login service
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import orjson
import heapq
import datetime
import time

# NOC modules
from noc.core.service.fastapi import FastAPIService
from noc.config import config
from noc.core.liftbridge.message import Message
from noc.services.login.auth import get_exp_from_jwt


class LoginService(FastAPIService):
    name = "login"
    process_name = "noc-%(name).10s-%(instance).2s"
    use_mongo = True
    use_translation = True
    if config.features.traefik:
        traefik_backend = "login"
        traefik_frontend_rule = "PathPrefix:/api/login,/api/auth/auth"

    OPENAPI_TAGS_DOCS = {
        "login": "Authentication services",
        "ext-ui": "Legacy ExtJS UI services. To be removed with decline of legacy UI",
    }

    def __init__(self):
        self.revoked_tokens = set()
        self.revoked_expiry = []

    def revoke_token(self, token: str) -> str:
        """
        Mark token as revoked. Any futher use will be prohibited
        :param token:
        :return: str
        """
        ts = datetime.datetime.utcnow()
        if token in self.revoked_tokens:
            return "exists"
        exp = get_exp_from_jwt(token)
        msg = {
            "token": token,
            "ts": ts.isoformat(),
            "expired": exp.isoformat(),
        }
        self.publish(orjson.encode(msg).encode("ascii"), "revokedtokens", 0)
        e2e = (datetime.datetime.utcnow() - ts).total_seconds()
        sec = e2e * 3 if e2e * 3 > 1 else 1
        time.sleep(sec)
        return "ok"

    def is_revoked(self, token: str) -> bool:
        """
        Check if token is revoked
        :param token: encoded JWT token to check
        :return: True if token is revoked
        """
        return token in self.revoked_tokens

    async def on_revoked_token(self, msg: Message) -> None:
        msg_dict = orjson.decode(msg.value)
        self.revoked_tokens.add(msg_dict["token"])
        heapq.heappush(
            self.revoked_expiry,
            (
                datetime.datetime.strptime(msg_dict["expired"], "%Y-%m-%dT%H:%M:%S%z"),
                msg_dict["token"],
            ),
        )
        # Check expired tokens
        heapq.heapify(self.revoked_expiry)
        for r in self.revoked_expiry.copy():
            if r[0] >= datetime.datetime.utcnow():
                break
            self.revoked_tokens.remove(r[1])
            heapq.heappop(self.revoked_expiry)

    async def on_activate(self):
        await self.subscribe_stream("revokedtokens", 0, self.on_revoked_token)


if __name__ == "__main__":
    LoginService().start()
