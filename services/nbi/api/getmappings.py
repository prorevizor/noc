# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# nbi getmappings API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# Third-party modules
import tornado.gen
import ujson
import six

# NOC modules
from noc.sa.interfaces.base import StringParameter, DictParameter
from noc.core.service.apiaccess import authenticated
from noc.models import get_model
from noc.main.models.remotesystem import RemoteSystem
from ..base import NBIAPI


class GetMappingsAPI(NBIAPI):
    name = "getmappings"
    SCOPES = {"managedobject": "sa.ManagedObject"}

    @authenticated
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.to_executor(self.do_post)

    @authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        print(self.request.arguments)
        scope = self.get_argument("scope", None)
        if not scope:
            self.write_result(400, self.error_msg("Missed scope"))
            raise tornado.gen.Return()
        id = self.get_argument("id", None)
        if id:
            # Search by local_id
            yield self.to_executor(self.do_mapping, scope=scope, id=id)
        else:
            # Search by remote_system
            remote_system = self.get_argument("remote_system", None)
            if not remote_system:
                self.write_result(400, self.error_msg("Either id or remote_system is missed"))
                raise tornado.gen.Return()
            remote_id = self.get_argument("remote_id", None)
            if not remote_system:
                self.write_result(400, self.error_msg("Either id or remote_id is missed"))
                raise tornado.gen.Return()
            yield self.to_executor(
                self.do_mapping, scope=scope, remote_system=remote_system, remote_id=remote_id
            )

    @tornado.gen.coroutine
    def to_executor(self, handler, *args, **kwargs):
        """
        Continue processing on executor
        :param handler:
        :param args:
        :param kwargs:
        :return:
        """
        code, result = yield self.executor.submit(handler, *args, **kwargs)
        self.write_result(code, result)

    def write_result(self, code, result):
        self.set_status(code)
        if isinstance(result, six.string_types):
            self.write(result)
        else:
            self.set_header("Content-Type", "text/json")
            self.write(ujson.dumps(result))

    @staticmethod
    def error_msg(msg):
        return {"status": False, "error": msg}

    def do_post(self):
        # Decode request
        try:
            req = ujson.loads(self.request.body)
        except ValueError:
            return 400, self.error_msg("Cannot decode JSON")
        # Validate
        try:
            req = Request.clean(req)
        except ValueError as e:
            return 400, self.error_msg("Bad request: %s" % e)
        return self.do_mapping(**req)

    def do_mapping(self, scope, id=None, remote_system=None, remote_id=None, **kwargs):
        """
        Perform mapping
        :param scope: scope name
        :param id: Local id
        :param remote_system: Remote system id
        :param remote_id: Id from remote system
        :param kwargs: Ignored args
        :return:
        """

        def format_obj(o):
            r = {"scope": scope, "id": str(o.id), "mappings": []}
            if o.remote_system:
                r["mappings"] += [
                    {"remote_system": str(o.remote_system.id), "remote_id": str(o.remote_id)}
                ]
            return r

        model = get_model(self.SCOPES[scope])
        if not model:
            return 400, self.error_msg("Invalid scope")
        if id is not None:
            qs = model.objects.filter(id=id)
        elif remote_system is not None and remote_id is not None:
            rs = RemoteSystem.get_by_id(remote_system)
            if not rs:
                return 404, self.error_msg("Remote system not found")
            qs = model.objects.filter(remote_system=rs.id, remote_id=remote_id)
        else:
            return 400, self.error_msg("Bad request")
        result = [format_obj(o) for o in qs]
        if not result:
            return 404, self.error_msg("Not found")
        return 200, result


RequestByLocal = DictParameter(
    attrs={"scope": StringParameter(choices=list(GetMappingsAPI.SCOPES)), "id": StringParameter()}
)

RequestByRemote = DictParameter(
    attrs={
        "scope": StringParameter(choices=list(GetMappingsAPI.SCOPES)),
        "remote_system": StringParameter(),
        "remote_id": StringParameter(),
    }
)

Request = RequestByLocal | RequestByRemote
