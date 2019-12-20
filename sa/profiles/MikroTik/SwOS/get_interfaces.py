# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# MikroTik.SwOS.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces


class Script(BaseScript):
    name = "MikroTik.SwOS.get_interfaces"
    interface = IGetInterfaces

    PORT_RANGE = 33

    def execute(self):
        interfaces = []
        links = self.profile.parseBrokenJson(self.http.get("/link.b", cached=True, eof_mark="}"))
        vlans = self.profile.parseBrokenJson(self.http.get("/vlan.b", cached=True, eof_mark="}"))
        fwds = self.profile.parseBrokenJson(self.http.get("/fwd.b", cached=True, eof_mark="}"))
        prt = int(links["prt"], 16)
        sfp = int(links.get("sfp", "0x0"), 16)
        sfpo = int(links.get("sfpo", "0x0"), 16)
        if sfpo + sfp != prt:
            raise self.UnexpectedResultError("prt=%d sfp=%d sfpo=%d" % (prt, sfp, sfpo))

        BITS = dict((i, 2 ** i) for i in range(self.PORT_RANGE))
        oper_statuses = dict(
            (i, bool(int(links["lnk"], 16) & BITS[i])) for i in range(self.PORT_RANGE)
        )
        admin_statuses = dict(
            (i, bool(int(links["an"], 16) & BITS[i])) for i in range(self.PORT_RANGE)
        )

        for port in range(1, prt + 1):
            if port <= sfpo:
                ifname = "Port%d" % int(port)
            else:
                ifname = "SFP%d" % (int(port) - sfpo)
            iface = {
                "name": ifname,
                "description": links["nm"][port - 1].decode("hex"),
                "type": "physical",
                "oper_status": oper_statuses[port - 1],
                "admin_status": admin_statuses[port - 1],
            }
            sub = {
                "name": ifname,
                "description": links["nm"][port - 1].decode("hex"),
                "enabled_afi": ["BRIDGE"],
                "oper_status": oper_statuses[port - 1],
                "admin_status": admin_statuses[port - 1],
            }
            tagged_vlans = []
            for vlan in vlans:
                vid = int(vlan["vid"], 16)
                ports = dict(
                    (i, bool(int(vlan["mbr"], 16) & BITS[i])) for i in range(self.PORT_RANGE)
                )
                if ports[port - 1]:
                    tagged_vlans += [vid]
            untagged = int(fwds["dvid"][port - 1], 16)
            if int(fwds["vlni"][port - 1], 16) != 1:  # only tagged
                sub["untagged_vlan"] = untagged
            if int(fwds["vlni"][port - 1], 16) != 2:  # only untagged
                sub["tagged_vlans"] = tagged_vlans
            iface["subinterfaces"] = [sub]
            interfaces += [iface]

        return [{"interfaces": interfaces}]
