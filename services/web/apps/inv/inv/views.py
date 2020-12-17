# ---------------------------------------------------------------------
# inv.inv application
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import inspect
import os
from typing import Optional, Dict, List, Any

# NOC modules
from noc.lib.app.extapplication import ExtApplication, view
from noc.inv.models.object import Object
from noc.inv.models.error import ConnectionError
from noc.inv.models.objectmodel import ObjectModel, ConnectionType, ModelConnectionsCache
from noc.core.validators import is_objectid
from noc.sa.interfaces.base import (
    StringParameter,
    ObjectIdParameter,
    UnicodeParameter,
    ListOfParameter,
    BooleanParameter,
)
from noc.core.translation import ugettext as _


class InvApplication(ExtApplication):
    """
    inv.inv application
    """

    title = _("Inventory")
    menu = _("Inventory")

    # Undeletable nodes
    UNDELETABLE = {
        # Global Lost&Found
        "b0fae773-b214-4edf-be35-3468b53b03f2"
    }

    def __init__(self, *args, **kwargs):
        ExtApplication.__init__(self, *args, **kwargs)
        # Load plugins
        from .plugins.base import InvPlugin

        self.plugins = {}
        for f in os.listdir("services/web/apps/inv/inv/plugins/"):
            if not f.endswith(".py") or f == "base.py" or f.startswith("_"):
                continue
            mn = "noc.services.web.apps.inv.inv.plugins.%s" % f[:-3]
            m = __import__(mn, {}, {}, "*")
            for on in dir(m):
                o = getattr(m, on)
                if inspect.isclass(o) and issubclass(o, InvPlugin) and o.__module__.startswith(mn):
                    assert o.name
                    self.plugins[o.name] = o(self)

    def get_plugin_data(self, name):
        return {"name": name, "xtype": self.plugins[name].js}

    @view("^node/$", method=["GET"], access="read", api=True)
    def api_node(self, request):
        children = []
        if request.GET and "node" in request.GET:
            container = request.GET["node"]
            if is_objectid(container):
                container = Object.get_by_id(container)
                if not container:
                    return self.response_not_found()
                children = [(o.name, o) for o in Object.objects.filter(container=container.id)]
                # Collect inner connections
                children += [(name, o) for name, o, _ in container.get_inner_connections()]
            elif container == "root":
                cmodels = [
                    d["_id"]
                    for d in ObjectModel._get_collection().find(
                        {"data.container.container": True}, {"_id": 1}
                    )
                ]
                children = [
                    (o.name, o)
                    for o in Object.objects.filter(
                        __raw__={"container": None, "model": {"$in": cmodels}}
                    )
                ]

            else:
                return self.response_bad_request()
        r = []
        # Build node interface
        for name, o in children:
            m_plugins = o.model.plugins or []
            disabled_plugins = set(p[1:] for p in m_plugins if p.startswith("-"))
            n = {
                "id": str(o.id),
                "name": name,
                "plugins": [],
                "can_add": bool(o.get_data("container", "container")),
                "can_delete": str(o.model.uuid) not in self.UNDELETABLE,
            }
            if o.get_data("container", "container") or o.has_inner_connections():
                # n["expanded"] = Object.objects.filter(container=o.id).count() == 1
                n["expanded"] = False
            else:
                n["leaf"] = True
            if o.get_data("rack", "units"):
                n["plugins"] += [self.get_plugin_data("rack")]
            if o.model.connections:
                n["plugins"] += [self.get_plugin_data("inventory")]
            if o.get_data("geopoint", "layer"):
                n["plugins"] += [self.get_plugin_data("map")]
            if o.get_data("management", "managed_object"):
                n["plugins"] += [self.get_plugin_data("managedobject")]
            if o.get_data("contacts", "has_contacts"):
                n["plugins"] += [self.get_plugin_data("contacts")]
            # Append model's plugins
            for p in m_plugins:
                if not p.startswith("-"):
                    n["plugins"] += [self.get_plugin_data(p)]
            n["plugins"] += [
                self.get_plugin_data("data"),
                self.get_plugin_data("comment"),
                self.get_plugin_data("file"),
                self.get_plugin_data("log"),
            ]
            # Process disabled plugins
            n["plugins"] = [p for p in n["plugins"] if p["name"] not in disabled_plugins]
            r += [n]
        return r

    @view(
        "^add_group/$",
        method=["POST"],
        access="create_group",
        api=True,
        validate={
            "container": ObjectIdParameter(required=False),
            "type": ObjectIdParameter(),
            "name": UnicodeParameter(),
            "serial": UnicodeParameter(required=False),
        },
    )
    def api_add_group(self, request, type, name, container=None, serial=None):
        if is_objectid(container):
            c = Object.get_by_id(container)
            if not c:
                return self.response_not_found()
            c = c.id
        elif container:
            return self.response_bad_request()
        else:
            c = None
        m = ObjectModel.get_by_id(type)
        if not m:
            return self.response_not_found()
        o = Object(name=name, model=m, container=c)
        if serial and m.get_data("asset", "part_no0"):
            o.set_data("asset", "serial", serial)
        o.save()
        o.log("Created", user=request.user.username, system="WEB", op="CREATE")
        return str(o.id)

    @view(
        "^remove_group/$",
        method=["DELETE"],
        access="remove_group",
        api=True,
        validate={"container": ObjectIdParameter(required=True)},
    )
    def api_remove_group(self, request, container=None):
        c = self.get_object_or_404(Object, id=container)
        c.delete()
        return True

    @view(
        "^insert/$",
        method=["POST"],
        access="reorder",
        api=True,
        validate={
            "container": ObjectIdParameter(required=False),
            "objects": ListOfParameter(element=ObjectIdParameter()),
            "position": StringParameter(),
        },
    )
    def api_insert(self, request, container, objects, position):
        """
        :param request:
        :param container: ObjectID after/in that insert
        :param objects: List ObjectID for insert
        :param position: 'append', 'before', 'after'
        :return:
        """
        c = self.get_object_or_404(Object, id=container)
        o = []
        for r in objects:
            o += [self.get_object_or_404(Object, id=r)]
        if position == "append":
            for x in o:
                x.put_into(c)
        elif position in ("before", "after"):
            cc = self.get_object_or_404(Object, id=c.container.id) if c.container else None
            for x in o:
                x.put_into(cc)
        return True

    @view("^(?P<id>[0-9a-f]{24})/path/$", method=["GET"], access="read", api=True)
    def api_get_path(self, request, id):
        o = self.get_object_or_404(Object, id=id)
        path = [{"id": str(o.id), "name": o.name}]
        while o.container:
            o = o.container
            path.insert(0, {"id": str(o.id), "name": o.name})
        return path

    @view(
        "^crossing_proposals/$",
        method=["GET"],
        access="read",
        api=True,
        validate={
            "o1": ObjectIdParameter(required=True),
            "o2": ObjectIdParameter(required=False),
            "left_filter": UnicodeParameter(required=False),
            "right_filter": UnicodeParameter(required=False),
            "cable_filter": UnicodeParameter(required=False),
        },
    )
    def api_get_crossing_proposals(
            self,
            request,
            o1,
            o2=None,
            left_filter: Optional[str] = None,
            right_filter: Optional[str] = None,
            cable_filter: Optional[str] = None,
    ):
        """
        For
        :param request:
        :param o1:
        :param o2:
        :param left_filter:
        :param right_filter:
        :param cable_filter:
        :return:
        """
        lo: Object = self.get_object_or_404(Object, id=o1)
        ro: Optional[Object] = None
        if o2:
            ro = self.get_object_or_404(Object, id=o2)
        lc: List[Dict[str, Any]] = []
        # Getting cable
        cables = ObjectModel.objects.filter(data__length__length__gte=0)
        # @todo filter cable for all current object slots
        for c in lo.model.connections:
            valid, disable_reason = True, ""
            if ro and right_filter:
                try:
                    lo.connect_p2p(c.name, ro, right_filter, {})
                except ConnectionError as e:
                    valid, disable_reason = False, str(e)
            oc, oo, _ = lo.get_p2p_connection(c.name)
            lc += [{
                "name": c.name,
                "type": str(c.type.id),
                "type__label": c.type.name,
                "gender": c.gender,
                "direction": c.direction,
                "protocols": c.protocols,
                "free": not bool(oc),
                "valid": valid,
                "disable_reason": disable_reason,
            }]
        rc: List[Dict[str, Any]] = []
        if ro:
            for c in ro.model.connections:
                valid, disable_reason = True, ""
                if left_filter:
                    try:
                        lo.connect_p2p(c.name, lo, left_filter, {})
                    except ConnectionError as e:
                        valid, disable_reason = False, str(e)
                oc, oo, _ = ro.get_p2p_connection(c.name)
                rc += [{
                    "name": c.name,
                    "type": str(c.type.id),
                    "type__label": c.type.name,
                    "gender": c.gender,
                    "direction": c.direction,
                    "protocols": c.protocols,
                    "free": not bool(oc),
                    "valid": valid,
                    "disable_reason": disable_reason,
                }]
        # Forming cable
        return {
            "left": {"connections": lc},
            "right": {"connections": rc},
            "cable": [{"name": c.name, "available": True} for c in cables],
            "valid": lc and rc and left_filter and right_filter,
        }

    @view(
        "^connect/$",
        method=["POST"],
        access="connect",
        api=True,
        validate={
            "object": ObjectIdParameter(required=True),
            "name": StringParameter(required=True),
            "remote_object": ObjectIdParameter(required=True),
            "remote_name": StringParameter(required=True),
            "cable": ObjectIdParameter(required=False),
            "reconnect": BooleanParameter(default=False, required=False),
        },
    )
    def api_connect(
            self,
            request,
            object,
            name,
            remote_object,
            remote_name,
            cable: Optional[str] = None,
            reconnect=False,
    ):
        lo: Object = self.get_object_or_404(Object, id=object)
        ro: Object = self.get_object_or_404(Object, id=remote_object)
        try:
            lo.connect_p2p(name, ro, remote_name, {})
        except ConnectionError as e:
            return self.render_json({"status": False, "text": str(e)})
        return True
