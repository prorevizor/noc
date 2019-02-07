# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Beward.BD.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
from noc.core.ip import IPv4


class Script(BaseScript):
    name = "Beward.BD.get_interfaces"
    interface = IGetInterfaces

    def execute(self):

        res = self.http.get("/cgi-bin/admin/param.cgi?action=list", json=False, cached=True, use_basic=True)
        r = {}
        for x in res.splitlines():
            if not x:
                continue
            k, v = x.split("=")
            r[k] = v

        interfaces = []
        ifname = "eth0"
        status = "Up"
#        enabled_afi = ["IPv4"]
        mac = r["root.Network.eth0.MACAddress"]
        ip = r["root.Network.eth0.IPAddress"]
        mask = r["root.Network.eth0.SubnetMask"]
        ip_addr = IPv4(ip, netmask=mask).prefix

        iface = {
            "name": ifname,
            "type": "physical",
            "admin_status": status == "Up",
            "oper_status": status == "Up",
            "subinterfaces": [{
                "name": ifname,
                "admin_status": status == "Up",
                "oper_status": status == "Up",
                "ipv4_addresses": [ip_addr],
                "mac": mac
            }]
        }
        interfaces += [iface]
        return [{"interfaces": interfaces}]
