#!./bin/python
# ---------------------------------------------------------------------
# Login service
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import orjson
import heapq
import datetime

# NOC modules
from noc.core.service.fastapi import FastAPIService
from noc.config import config
from noc.core.liftbridge.message import Message


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

    revoked_tokens = set()
    revoked_expiry = []

    def revoke_token(token: str) -> None:
        """
        Mark token as revoked. Any futher use will be prohibited
        :param token:
        :return:
        """

    def is_revoked(token: str) -> bool:
        """
        Check if token is revoked
        :param token: encoded JWT token to check
        :return: True if token is revoked
        """
        return False

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
        for r in self.revoked_expiry:
            if r[0] < datetime.datetime.now():
                self.revoked_tokens.remove(r)
                heapq.heappop(self.revoked_expiry)
            else:
                break
        return

    async def on_activate(self):
        await self.subscribe_stream("revokedtokens", 0, self.on_revoked_token)


if __name__ == "__main__":
    LoginService().start()
