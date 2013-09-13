# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## sa.managedobject application
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
from collections import defaultdict
## Django modules
from django.http import HttpResponse
## NOC modules
from noc.lib.app import ExtModelApplication, view
from noc.sa.models import ManagedObject, ManagedObjectAttribute
from noc.inv.models.link import Link
from noc.inv.models.interface import Interface
from noc.inv.models.interfaceprofile import InterfaceProfile
from noc.inv.models.subinterface import SubInterface
from noc.inv.models.pendinglinkcheck import PendingLinkCheck
from noc.lib.app.modelinline import ModelInline
from noc.lib.app.repoinline import RepoInline
from noc.main.models.resourcestate import ResourceState
from noc.project.models.project import Project
from noc.vc.models.vcdomain import VCDomain
from mongoengine.queryset import Q as MQ
from noc.lib.serialize import json_decode
from noc.lib.scheduler.utils import (get_job, refresh_schedule,
                                     submit_job)
from noc.lib.text import split_alnum


class ManagedObjectApplication(ExtModelApplication):
    """
    ManagedObject application
    """
    title = "Managed Objects"
    menu = "Managed Objects"
    model = ManagedObject
    query_condition = "icontains"
    # Inlines
    attrs = ModelInline(ManagedObjectAttribute)
    cfg = RepoInline("config")

    extra_permissions = ["alarm", "change_interface"]

    mrt_config = {
        "console": {
            "access": "console",
            "map_script": "commands",
            "timeout": 60
        }
    }

    DISCOVERY_METHODS = [
        ("enable_version_inventory", "version_inventory", None),
        ("enable_id_discovery", "id_discovery", None),
        ("enable_config_polling", "config_discovery", None),
        ("enable_interface_discovery", "interface_discovery", None),
        ("enable_vlan_discovery", "vlan_discovery", None),
        ("enable_lldp_discovery", "lldp_discovery", "lldp"),
        ("enable_bfd_discovery", "bfd_discovery", "bfd"),
        ("enable_stp_discovery", "stp_discovery", "stp"),
        ("enable_cdp_discovery", "cdp_discovery", "cdp"),
        ("enable_oam_discovery", "oam_discovery", "oam"),
        ("enable_rep_discovery", "rep_discovery", "rep"),
        ("enable_ip_discovery", "ip_discovery", None),
        ("enable_mac_discovery", "mac_discovery", "mac")
    ]

    def field_platform(self, o):
        return o.platform

    def field_row_class(self, o):
        return o.object_profile.style.css_class_name if o.object_profile.style else ""

    def field_interface_count(self, o):
        return Interface.objects.filter(managed_object=o.id, type="physical").count()

    def field_link_count(self, o):
        return Link.object_links_count(o)

    @view(url="^(?P<id>\d+)/links/$", method=["GET"],
          access="read", api=True)
    def api_links(self, request, id):
        o = self.get_object_or_404(ManagedObject, id=id)
        # Get links
        result = []
        for link in Link.object_links(o):
            l = []
            r = []
            for i in link.interfaces:
                if i.managed_object.id == o.id:
                    l += [i]
                else:
                    r += [i]
                for li, ri in zip(l, r):
                    result += [{
                        "id": str(link.id),
                        "local_interface": str(li.id),
                        "local_interface__label": li.name,
                        "remote_object": ri.managed_object.id,
                        "remote_object__label": ri.managed_object.name,
                        "remote_interface": str(ri.id),
                        "remote_interface__label": ri.name,
                        "discovery_method": link.discovery_method,
                        "commited": True,
                        "local_description": li.description,
                        "remote_description": ri.description
                    }]
        # Get pending links
        q = MQ(local_object=o.id) | MQ(remote_object=o.id)
        for link in PendingLinkCheck.objects.filter(q):
            if link.local_object.id == o.id:
                ro = link.remote_object
                lin = link.local_interface
                rin = link.remote_interface
            else:
                ro = link.local_object
                lin = link.remote_interface
                rin = link.local_interface
            li = Interface.objects.filter(managed_object=o.id, name=lin).first()
            if not li:
                continue
            ri = Interface.objects.filter(managed_object=ro.id, name=rin).first()
            if not ri:
                continue
            result += [{
                "id": str(link.id),
                "local_interface": str(li.id),
                "local_interface__label": li.name,
                "remote_object": ro.id,
                "remote_object__label": ro.name,
                "remote_interface": str(ri.id),
                "remote_interface__label": ri.name,
                "discovery_method": link.method,
                "commited": False,
                "local_description": li.description,
                "remote_description": ri.description
            }]
        return result

    @view(url="^link/approve/$", method=["POST"],
          access="change_link", api=True)
    def api_link_approve(self, request):
        d = json_decode(request.raw_post_data)
        plc = self.get_object_or_404(PendingLinkCheck, id=d.get("link"))
        li = Interface.objects.filter(
            managed_object=plc.local_object.id,
            name=plc.local_interface
            ).first()
        if not li:
            return {
                "success": False,
                "error": "Interface not found: %s:%s" % (
                    plc.local_object.name, plc.local_interface)
            }
        ri = Interface.objects.filter(
            managed_object=plc.remote_object.id,
            name=plc.remote_interface
            ).first()
        if not ri:
            return {
                "success": False,
                "error": "Interface not found: %s:%s" % (
                    plc.remote_object.name, plc.remote_interface)
            }
        li.link_ptp(ri, method=plc.method + "+manual")
        plc.delete()
        return {
            "success": True
        }

    @view(url="^link/reject/$", method=["POST"],
          access="change_link", api=True)
    def api_link_reject(self, request):
        d = json_decode(request.raw_post_data)
        plc = self.get_object_or_404(PendingLinkCheck, id=d.get("link"))
        plc.delete()
        return {
            "success": True
        }

    def check_mrt_access(self, request, name):
        # @todo: Check object's access
        return super(ManagedObjectApplication, self).check_mrt_access(request, name)

    @view(url="^(?P<id>\d+)/discovery/$", method=["GET"],
          access="read", api=True)
    def api_discovery(self, request, id):
        def iso(t):
            if t:
                return t.replace(tzinfo=self.TZ).isoformat()
            else:
                return None

        o = self.get_object_or_404(ManagedObject, id=id)
        link_count = defaultdict(int)
        for link in Link.object_links(o):
            m = link.discovery_method
            if "+" in m:
                m = m.split("+")[0]
            link_count[m] += 1
        r = []
        print link_count
        for cfg, name, method in self.DISCOVERY_METHODS:
            job = get_job("inv.discovery", name, o.id) or {}
            d = {
                "name": name,
                "enable_profile": getattr(o.object_profile, cfg),
                "status": job.get("s"),
                "last_run": iso(job.get("last")),
                "last_status": job.get("ls"),
                "next_run": iso(job.get("ts")),
                "link_count": link_count[method]
            }
            r += [d]
        return r

    @view(url="^(?P<id>\d+)/discovery/run/$", method=["POST"],
          access="change_discovery", api=True)
    def api_run_discovery(self, request, id):
        o = self.get_object_or_404(ManagedObject, id=id)
        r = json_decode(request.raw_post_data).get("names", [])
        d = 0
        for cfg, name, method in self.DISCOVERY_METHODS:
            if getattr(o.object_profile, cfg):
                if name in r:
                    refresh_schedule("inv.discovery",
                                     name, o.id, delta=d)
                    d += 1
        return {
            "success": True
        }

    @view(url="^(?P<id>\d+)/interface/$", method=["GET"],
        access="read", api=True)
    def api_interface(self, request, id):
        """
        GET interfaces
        :param managed_object:
        :return:
        """
        def sorted_iname(s):
            return sorted(s, key=lambda x: split_alnum(x["name"]))

        def get_style(i):
            profile = i.profile
            if profile:
                try:
                    return style_cache[profile.id]
                except KeyError:
                    pass
                if profile.style:
                    s = profile.style.css_class_name
                else:
                    s = ""
                style_cache[profile.id] = s
                return s
            else:
                return ""

        def get_link(i):
            link = i.link
            if not link:
                return None
            if link.is_ptp:
                # ptp
                o = link.other_ptp(i)
                label = "%s:%s" % (o.managed_object.name, o.name)
            elif link.is_lag:
                # unresolved LAG
                o = [ii for ii in link.other(i)
                     if ii.managed_object.id != i.managed_object.id]
                label = "LAG %s: %s" % (o[0].managed_object.name,
                                        ", ".join(ii.name for ii in o))
            else:
                # Broadcast
                label = ", ".join(
                    "%s:%s" % (ii.managed_object.name, ii.name)
                               for ii in link.other(i))
            return {
                "id": str(link.id),
                "label": label
            }

        # Get object
        o = self.get_object_or_404(ManagedObject, id=int(id))
        if not o.has_access(request.user):
            return self.response_forbidden("Permission denied")
        # Physical interfaces
        # @todo: proper ordering
        default_state = ResourceState.get_default()
        style_cache = {}  ## profile_id -> css_style
        l1 = [
            {
                "id": str(i.id),
                "name": i.name,
                "description": i.description,
                "mac": i.mac,
                "ifindex": i.ifindex,
                "lag": (i.aggregated_interface.name
                        if i.aggregated_interface else ""),
                "link": get_link(i),
                "profile": str(i.profile.id) if i.profile else None,
                "profile__label": unicode(i.profile) if i.profile else None,
                "enabled_protocols": i.enabled_protocols,
                "project": i.project.id if i.project else None,
                "project__label": unicode(i.project) if i.project else None,
                "state": i.state.id if i.state else default_state.id,
                "state__label": unicode(i.state if i.state else default_state),
                "vc_domain": i.vc_domain.id if i.vc_domain else None,
                "vc_domain__label": unicode(i.vc_domain) if i.vc_domain else None,
                "row_class": get_style(i)
            } for i in Interface.objects.filter(
                managed_object=o.id, type="physical")
        ]
        # LAG
        lag = [
            {
                "name": i.name,
                "description": i.description,
                "members": [j.name for j in Interface.objects.filter(
                    managed_object=o.id, aggregated_interface=i.id)]
            } for i in
              Interface.objects.filter(managed_object=o.id,
                                       type="aggregated")
        ]
        # L2 interfaces
        l2 = [
            {
                "name": i.name,
                "description": i.description,
                "untagged_vlan": i.untagged_vlan,
                "tagged_vlans": i.tagged_vlans
            } for i in
              SubInterface.objects.filter(managed_object=o.id,
                  enabled_afi="BRIDGE")
        ]
        # L3 interfaces
        q = MQ(enabled_afi="IPv4") | MQ(enabled_afi="IPv6")
        l3 = [
            {
                "name": i.name,
                "description": i.description,
                "ipv4_addresses": i.ipv4_addresses,
                "ipv6_addresses": i.ipv6_addresses,
                "enabled_protocols": i.enabled_protocols,
                "vlan": i.vlan_ids,
                "vrf": i.forwarding_instance.name if i.forwarding_instance else ""
            } for i in
              SubInterface.objects.filter(managed_object=o.id).filter(q)
        ]
        return {
            "l1": sorted_iname(l1),
            "lag": sorted_iname(lag),
            "l2": sorted_iname(l2),
            "l3": sorted_iname(l3)
        }

    @view(url="^(?P<id>\d+)/interface/$", method=["POST"],
        access="change_interface", api=True)
    def api_set_interface(self, request, id):
        def get_or_none(c, v):
            if not v:
                return None
            return c.objects.get(id=v)
        o = self.get_object_or_404(ManagedObject, id=int(id))
        d = json_decode(request.raw_post_data)
        if "id" in d:
            i = self.get_object_or_404(Interface, id=d["id"])
            if i.managed_object.id != o.id:
                return self.response_not_found()
            # Set profile
            if "profile" in d:
                p = get_or_none(InterfaceProfile, d["profile"])
                i.profile = p
                if p:
                    i.profile_locked = True
            # Project
            if "project" in d:
                i.project = get_or_none(Project, d["project"])
            # State
            if "state" in d:
                i.state = get_or_none(ResourceState, d["state"])
            # VC Domain
            if "vc_domain" in d:
                i.vc_domain = get_or_none(VCDomain, d["vc_domain"])
            #
            i.save()
        return {
            "success": True
        }

    @view(method=["DELETE"], url="^(?P<id>\d+)/?$", access="delete", api=True)
    def api_delete(self, request, id):
        """
        Override default method
        :param request:
        :param id:
        :return:
        """
        try:
            o = self.queryset(request).get(id=int(id))
        except self.model.DoesNotExist:
            return self.render_json({
                "status": False,
                "message": "Not found"
            }, status=self.NOT_FOUND)
        # Run sa.wipe_managed_object job instead
        o.name = "wiping-%d" % o.id
        o.is_managed = False
        o.description = "Wiping! Do not touch!"
        o.save()
        submit_job("main.jobs", "sa.wipe_managedobject", key=o.id)
        return HttpResponse(status=self.DELETED)
