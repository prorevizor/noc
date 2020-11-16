# ---------------------------------------------------------------------
# HP.Comware.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
from noc.core.text import parse_kv


class Script(BaseScript):
    name = "HP.Comware.get_interfaces"
    interface = IGetInterfaces

    rx_mtu = re.compile(r"The Maximum Frame Length is (?P<mtu>\d+)")
    rx_port_type = re.compile(r"Port link-type: (?P<port_type>hybrid|access|trunk)")
    rx_port_other = re.compile(
        r"^\s*Tagged\s+VLAN ID : (?P<tagged>[^\n]+)\n"
        r"^\s*Untagged VLAN ID : (?P<untagged>[^\n]+)\n",
        re.MULTILINE,
    )
    rx_port_trunk = re.compile(
        r"^\s*VLAN passing\s+: (?P<passing>[^\n]+)\n"
        r"^\s*VLAN permitted: (?P<permitted>[^\n]+)\n",
        re.MULTILINE,
    )
    rx_ip = re.compile(r"Internet Address is (?P<ip>\S+) Primary")
    rx_ips = re.compile(r"Internet Address is (?P<ip>\S+) Sub")
    rx_mac = re.compile(
        r"IP (?:Packet Frame Type:|Sending Frames' Format is) PKTFMT_ETHNT_2, Hardware Address(?: is|:) (?P<mac>\S+)"
    )

    rx_vlan_name = re.compile(r"^Vlan-interface(?P<vlan>\d+)?")
    rx_isis = re.compile(r"Interface:\s+(?P<iface>\S+)")
    rx_sub_default_vlan = re.compile(r"\(default vlan\),?")
    rx_parse_interface_vlan = re.compile(r"(\d+)(?:\(.+\))?")

    def get_isis_interfaces(self):
        r = []
        try:
            v = self.cli("display isis interface")
            for match in self.rx_isis.finditer(v):
                r += [match.group("iface")]
        except self.CLISyntaxError:
            pass
        return r

    interface_map = {
        "current state": "oper_status",
        "line protocol state": "line_status",
        "description": "description",
        "maximum transmit unit": "mtu",
        "port link-type": "port_type",
        "pvid": "pvid",
        "untagged vlan id": "untagged_vlan",
        "tagged vlan id": "tagged_vlan",
        "vlan passing": "vlan_passing",
        "vlan permitted": "vlan_permitted",
    }

    def parse_interface_block(self, block):
        r = parse_kv(self.interface_map, block)
        if "mtu" not in r and self.rx_mtu.search(block):
            r["mtu"] = self.rx_mtu.search(block).group(1)
        if self.rx_mac.search(block):
            r["mac"] = self.rx_mac.search(block).group(1)
        ip_match = self.rx_ip.search(block)
        if ip_match:
            r["ip"] = ip_match.group(1)
        if "tagged_vlan" in r and self.rx_sub_default_vlan.search(r["tagged_vlan"]):
            r["tagged_vlan"] = r["tagged_vlan"].replace("(default vlan)", "")
        if "vlan_passing" in r and self.rx_sub_default_vlan.search(r["vlan_passing"]):
            r["vlan_passing"] = r["vlan_passing"].replace("(default vlan)", "")
        if "untagged_vlan" in r:
            r["untagged_vlan"] = self.rx_parse_interface_vlan.match(r["untagged_vlan"]).group(1)
        return r

    def execute_cli(self, **kwargs):
        isis = self.get_isis_interfaces()

        # Get portchannels
        portchannel_members = {}
        for pc in self.scripts.get_portchannel():
            i = pc["interface"]
            t = pc["type"] == "L"
            for m in pc["members"]:
                portchannel_members[m] = (i, t)
        interfaces = {}
        v = self.cli("display interface")
        # "display interface Vlan-interface"
        # "display interface NULL"
        for block in v.split("\n\n"):
            if not block.strip():
                continue
            ifname, block = block.split(None, 1)
            if ifname in interfaces:
                continue
            r = self.parse_interface_block(block)
            if not r:
                continue
            iftype = self.profile.get_interface_type(ifname)
            self.logger.info("Process interface: %s", ifname)
            o_status = r.get("oper_status", "").lower() == "up"
            a_status = False if "DOWN ( Administratively)" in r.get("oper_status", "") else True
            name = ifname
            if "." in ifname:
                ifname, vlan_ids = ifname.split(".", 1)
            else:
                interfaces[ifname] = {
                    "name": ifname,
                    "type": iftype,
                    "admin_status": a_status,
                    "oper_status": o_status,
                    "enabled_protocols": [],
                    "subinterfaces": [],
                }
                if "description" in r:
                    interfaces[ifname]["description"] = r["description"]
                if "mac" in r:
                    interfaces[ifname]["mac"] = r["mac"]
                if ifname in portchannel_members:
                    ai, is_lacp = portchannel_members[ifname]
                    interfaces[ifname]["aggregated_interface"] = ai
                    interfaces[ifname]["enabled_protocols"] += ["LACP"]

            sub = {
                "name": name,
                "admin_status": a_status,
                "oper_status": o_status,
                "enabled_protocols": [],
                "enabled_afi": [],
            }
            if ifname in isis:
                sub["enabled_protocols"] += ["ISIS"]
            if "mac" in r:
                sub["mac"] = r["mac"]
            if "ip" in r:
                sub["enabled_afi"] += ["IPv4"]
                sub["ipv4_addresses"] = [r["ip"]]
            if self.rx_vlan_name.match(name):
                sub["vlan_ids"] = [int(self.rx_vlan_name.match(name).group(1))]
            if "port_type" in r:
                sub["enabled_afi"] += ["BRIDGE"]
                # Bridge interface
                if r["port_type"] in ["access", "hybrid"] and "untagged_vlan" in r:
                    sub["untagged_vlan"] = int(r["untagged_vlan"])
                if r["port_type"] in ["access", "hybrid"] and "tagged_vlan" in r:
                    sub["tagged_vlan"] = self.expand_rangelist((r["tagged_vlan"]))
                if r["port_type"] == "trunk" and "vlan_passing" in r:
                    sub["tagged_vlan"] = self.expand_rangelist(r["vlan_passing"])
            interfaces[ifname]["subinterfaces"] += [sub]

        return [{"interfaces": list(interfaces.values())}]
