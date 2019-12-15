# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Alstec.ALS.get_spanning_tree
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetspanningtree import IGetSpanningTree


class Script(BaseScript):
    name = "Alstec.ALS.get_spanning_tree"
    interface = IGetSpanningTree

    rx_mode = re.compile(r"^\s*Spanning tree enabled mode (?P<mode>\S+)")
    rx_mstp = re.compile(
        r"^\s*Name: (?P<region>\S+)\s*\n" r"^\s*Revision: (?P<revision>\d+)", re.MULTILINE
    )
    rx_inst1 = re.compile(
        r"MST (?P<id>\d+) Vlans Mapped: (?P<vlans>.+?)\n"
        r"^\s*CST Root ID\s+Priority\s+(?P<root_priority>\d+)\s*\n"
        r"^\s*Address\s+(?P<root_id>\S+)\s*\n"
        r"^\s*Path Cost\s+(?:\d+)\s*\n"
        r"^\s*Root Port\s+(?:\S+)\s*\n"
        r"^\s*.+\n"
        r"(^\s*.+\n)?"
        r"^\s*Bridge ID\s+Priority\s+(?P<bridge_priority>\d+)\s*\n"
        r"^\s*Address\s+(?P<bridge_id>\S+)\s*\n",
        re.MULTILINE,
    )
    rx_inst2 = re.compile(
        r"^\s*Root ID\s+Priority\s+(?P<root_priority>\d+)\s*\n"
        r"^\s*Address\s+(?P<root_id>\S+)\s*\n"
        r"^\s*Cost\s+(?:\d+)\s*\n"
        r"^\s*Port\s+(?:\S+)\s*\n"
        r"^\s*Hello Time\s+.+\n"
        r"^\s*Bridge ID\s+Priority\s+(?P<bridge_priority>\d+)\s*\n"
        r"^\s*Address\s+(?P<bridge_id>\S+)\s*\n",
        re.MULTILINE,
    )
    rx_inst3 = re.compile(
        r"^\s*Root ID\s+Priority\s+(?P<root_priority>\d+)\s*\n"
        r"^\s*Address\s+(?P<root_id>\S+)\s*\n"
        r"^\s*This switch is the root\s*\n",
        re.MULTILINE,
    )
    rx_vlans = re.compile("^(?P<id>\d+)\s+(?P<vlans>\S+)\s+enabled", re.MULTILINE)
    rx_port = re.compile(
        r"^\s*Port (?P<interface>\S+) (?:enabled|disabled)\s*\n"
        r"^\s*State: (?P<state>\S+)\s+Role: (?P<role>\S+)\s*\n"
        r"^\s*Port id: (?P<port_id>\S+)\s+Port cost: (?P<priority>\d+)\s*\n"
        r"^\s*.+\n"
        r"^\s*Designated bridge Priority\s*: "
        r"(?P<designated_bridge_priority>\S+)\s+Address: "
        r"(?P<designated_bridge_id>\S+)\s*\n"
        r"^\s*Designated port id: (?P<designated_port_id>\S+)\s+"
        r"Designated path cost: \d+\s*\n",
        re.MULTILINE,
    )

    def execute_cli(self):
        try:
            v = self.cli("show spanning-tree detail")
        except self.CLISyntaxError:
            return {"mode": "None", "instances": []}
        match = self.rx_mode.search(v)
        mode = match.group("mode")
        stp = {"mode": mode, "instances": []}
        try:
            c = self.cli("show spanning-tree mst-configuration")
        except self.CLISyntaxError:
            c = ""
        if mode == "MSTP":
            match = self.rx_mstp.search(c)
            stp["configuration"] = {}
            stp["configuration"]["MSTP"] = match.groupdict()
            for instanses in v.split("######"):
                match = self.rx_inst1.search(instanses)
                if match:
                    inst = match.groupdict()
                    inst["interfaces"] = []
                    for port in instanses.split("\n\n"):
                        match = self.rx_port.search(port)
                        if match:
                            iface = match.groupdict()
                            iface["point_to_point"] = "Type: P2P" in port
                            iface["priority"] = match.group("port_id").split(".")[0]
                            iface["edge"] = False
                            inst["interfaces"] += [iface]
                    stp["instances"] += [inst]
        else:
            # STP or RSTP mode
            match = self.rx_inst2.search(v)
            if match:
                inst = match.groupdict()
            else:
                match = self.rx_inst3.search(v)  # This device is 'root'
                inst = match.groupdict()
                inst["bridge_priority"] = inst["root_priority"]
                inst["bridge_id"] = inst["root_id"]
            inst["id"] = 0
            inst["interfaces"] = []
            match = self.rx_vlans.search(c)
            if match:
                inst["vlans"] = match.group("vlans")
            else:
                inst["vlans"] = "1-4094"
            for port in v.split("\n\n"):
                match = self.rx_port.search(port)
                if match:
                    iface = match.groupdict()
                    iface["point_to_point"] = "Type: P2P" in port
                    iface["priority"] = match.group("port_id").split(".")[0]
                    iface["edge"] = False
                    inst["interfaces"] += [iface]
            stp["instances"] = [inst]
        return stp
