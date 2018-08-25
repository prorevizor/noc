# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Rotek.RTBS.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces


class Script(BaseScript):
    name = "Rotek.RTBS.get_interfaces"
    cache = True
    interface = IGetInterfaces

    rx_sh_int = re.compile(
        r"^(?P<ifindex>\d+):\s+(?P<ifname>(e|l|t|b|r|g|n)\S+):\s"
        r"<(?P<flags>.*?)>\s+mtu\s+(?P<mtu>\d+).+?\n"
        r"^\s+link/\S+(?:\s+(?P<mac>[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}))?\s+.+?\n"
        r"(?:^\s+inet\s+(?P<ip>\d+\S+)\s+)?", re.MULTILINE | re.DOTALL
    )

    rx_status = re.compile(r"^(?P<status>UP|DOWN\S+)", re.MULTILINE)

    def execute_snmp(self):
        interfaces = []
        ss = {}
        # SNMP
        for soid, sname in self.snmp.getnext("1.3.6.1.4.1.32761.3.5.1.2.1.1.4"):
            sifindex = int(soid.split(".")[-1])
            ieee_mode = self.snmp.get("1.3.6.1.4.1.32761.3.5.1.2.1.1.2.%s" % sifindex)
            freq = self.snmp.get("1.3.6.1.4.1.32761.3.5.1.2.1.1.7.%s" % sifindex)
            channel = self.snmp.get("1.3.6.1.4.1.32761.3.5.1.2.1.1.8.%s" % sifindex)
            channelbandwidth = self.snmp.get("1.3.6.1.4.1.32761.3.5.1.2.1.1.9.%s" % sifindex)
            ss[sifindex] = {
                "ssid": sname,
                "ieee_mode": ieee_mode,
                "channel": channel,
                "freq": freq,
                "channelbandwidth": channelbandwidth
            }

        for soid, sname in self.snmp.getnext("1.3.6.1.4.1.41752.3.5.1.2.1.1.4"):
            sifindex = int(soid.split(".")[-1])
            ieee_mode = self.snmp.get("1.3.6.1.4.1.41752.3.5.1.2.1.1.2.%s" % sifindex)
            freq = self.snmp.get("1.3.6.1.4.1.41752.3.5.1.2.1.1.7.%s" % sifindex)
            channel = self.snmp.get("1.3.6.1.4.1.41752.3.5.1.2.1.1.8.%s" % sifindex)
            channelbandwidth = self.snmp.get("1.3.6.1.4.1.41752.3.5.1.2.1.1.9.%s" % sifindex)
            ss[sifindex] = {
                "ssid": sname,
                "ieee_mode": ieee_mode,
                "channel": channel,
                "freq": freq,
                "channelbandwidth": channelbandwidth
            }

        for v in self.snmp.getnext("1.3.6.1.2.1.2.2.1.1", cached=True):
            ifindex = v[1]
            name = self.snmp.get("1.3.6.1.2.1.2.2.1.2.%s" % str(ifindex))
            iftype = self.profile.get_interface_type(name)
            if "peer" in name:
                continue
            if not name:
                self.logger.info("Ignoring unknown interface type: '%s", iftype)
                continue
            mac = self.snmp.get("1.3.6.1.2.1.2.2.1.6.%s" % str(ifindex))
            mtu = self.snmp.get("1.3.6.1.2.1.2.2.1.4.%s" % str(ifindex))
            astatus = self.snmp.get("1.3.6.1.2.1.2.2.1.7.%s" % str(ifindex))
            if astatus == 1:
                admin_status = True
            else:
                admin_status = False
            ostatus = self.snmp.get("1.3.6.1.2.1.2.2.1.8.%s" % str(ifindex))
            if ostatus == 1:
                oper_status = True
            else:
                oper_status = False
            iface = {
                "type": iftype,
                "name": name,
                "mac": mac,
                "admin_status": admin_status,
                "oper_status": oper_status,
                "snmp_ifindex": ifindex,
                "subinterfaces": [
                    {
                        "name": name,
                        "mac": mac,
                        "snmp_ifindex": ifindex,
                        "admin_status": admin_status,
                        "oper_status": oper_status,
                        "mtu": mtu,
                        "enabled_afi": ["BRIDGE"]
                    }
                ]
            }
            interfaces += [iface]
            for i in ss.items():
                if int(i[0]) == ifindex:
                    a = self.cli("show interface %s ssid-broadcast" % name)
                    sb = a.split(":")[1].strip()
                    if sb == "enabled":
                        ssid_broadcast = "Enable"
                    else:
                        ssid_broadcast = "Disable"
                    vname = "%s.%s" % (name, i[1]["ssid"])
                    iface = {
                        "type": "physical",
                        "name": vname,
                        "mac": mac,
                        "admin_status": admin_status,
                        "oper_status": oper_status,
                        "snmp_ifindex": ifindex,
                        "description": "ssid_broadcast=%s, ieee_mode=%s, channel=%s,"
                        "freq=%sGHz, channelbandwidth=%sMHz" % (
                            ssid_broadcast, i[1]["ieee_mode"], i[1]["channel"], i[1]["freq"],
                            i[1]["channelbandwidth"]
                        ),
                        "subinterfaces": [
                            {
                                "name": vname,
                                "mac": mac,
                                "snmp_ifindex": ifindex,
                                "admin_status": admin_status,
                                "oper_status": oper_status,
                                "mtu": mtu,
                                "enabled_afi": ["BRIDGE"]
                            }
                        ]
                    }
                    interfaces += [iface]
        return [{"interfaces": interfaces}]

    def execute_cli(self):
        interfaces = []
        ssid = {}
        # GO CLI
        i = ["ra0", "ra1"]
        for ri in i:
            s = self.cli("show interface %s ssid" % ri)
            v = self.cli("show interface %s vlan-to-ssid" % ri)
            if "vlan-to-ssid not configured" in v:
                continue
            a = self.cli("show interface %s ssid-broadcast" % ri)
            i = self.cli("show interface %s ieee-mode" % ri)
            c = self.cli("show interface %s channel" % ri)
            f = self.cli("show interface %s freq" % ri)
            res = s.split(":")[1].strip().replace("\"", "")
            resv = v.split(":")[1].strip().replace("\"", "")
            ssid_broadcast = a.split(":")[1].strip()
            ieee_mode = "IEEE 802.%s" % i.split(":")[1].strip()
            channel = c.split(":")[1].strip()
            freq = f.split(":")[1].strip()
            ssid[ri] = {
                "ssid": res,
                "vlan": resv,
                "ssid_broadcast": ssid_broadcast,
                "ieee_mode": ieee_mode,
                "channel": channel,
                "freq": freq
            }
        with self.profile.shell(self):
            v = self.cli("ip a", cached=True)
            for match in self.rx_sh_int.finditer(v):
                a_stat = True
                ifname = match.group("ifname")
                if "@" in ifname:
                    ifname = ifname.split("@")[0]
                flags = match.group("flags")
                smatch = self.rx_status.search(flags)
                if smatch:
                    o_status = smatch.group("status").lower() == "up"
                else:
                    o_status = True
                ip = match.group("ip")
                mac = match.group("mac")
                iface = {
                    "type": self.profile.get_interface_type(ifname),
                    "name": ifname,
                    "admin_status": a_stat,
                    "oper_status": o_status,
                    "snmp_ifindex": match.group("ifindex"),
                    "subinterfaces": [
                        {
                            "name": ifname,
                            "mtu": match.group("mtu"),
                            "admin_status": a_stat,
                            "oper_status": o_status,
                            "snmp_ifindex": match.group("ifindex"),
                        }
                    ]
                }
                if mac:
                    iface["mac"] = mac
                    iface["subinterfaces"][0]["mac"] = mac
                if ip:
                    iface["subinterfaces"][0]["address"] = ip
                    iface["subinterfaces"][0]["enabled_afi"] = ["IPv4"]
                else:
                    iface["subinterfaces"][0]["enabled_afi"] = ["BRIDGE"]
                interfaces += [iface]
                for ri in ssid.items():
                    if ifname in ri[0]:
                        iface = {
                            "type": "physical",
                            "name": "%s.%s" % (ifname, ri[1]["ssid"]),
                            "admin_status": a_stat,
                            "oper_status": o_status,
                            "mac": mac,
                            "snmp_ifindex": match.group("ifindex"),
                            "description": "ssid_broadcast=%s, ieee_mode=%s, channel=%s, freq=%s" %
                            (
                                ri[1]["ssid_broadcast"], ri[1]["ieee_mode"], ri[1]["channel"],
                                ri[1]["freq"]
                            ),
                            "subinterfaces": [
                                {
                                    "name": "%s.%s" % (ifname, ri[1]["ssid"]),
                                    "enabled_afi": ["BRIDGE"],
                                    "admin_status": a_stat,
                                    "oper_status": o_status,
                                    "mac": mac,
                                    "snmp_ifindex": match.group("ifindex"),
                                    "untagged_vlan": int(ri[1]["vlan"]),
                                }
                            ]
                        }
                        interfaces += [iface]
        return [{"interfaces": interfaces}]
