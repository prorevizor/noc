# ---------------------------------------------------------------------
# Extreme.XOS.get_lldp_neighbors
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
from collections import defaultdict

# NOC modules
from noc.sa.profiles.Generic.get_lldp_neighbors import Script as BaseScript
from noc.sa.interfaces.igetlldpneighbors import IGetLLDPNeighbors
from noc.sa.interfaces.base import MACAddressParameter
from noc.core.validators import is_int, is_ipv4, is_ipv6, is_mac
from noc.core.lldp import (
    LLDP_CHASSIS_SUBTYPE_MAC,
    LLDP_CHASSIS_SUBTYPE_NETWORK_ADDRESS,
    LLDP_CHASSIS_SUBTYPE_LOCAL,
    LLDP_PORT_SUBTYPE_MAC,
    LLDP_PORT_SUBTYPE_NETWORK_ADDRESS,
    LLDP_PORT_SUBTYPE_NAME,
    LLDP_PORT_SUBTYPE_LOCAL,
)


#
# @todo: SNMP Support
#


class Script(BaseScript):
    name = "Extreme.XOS.get_lldp_neighbors"
    interface = IGetLLDPNeighbors

    rx_lldp_nei = re.compile(
        r"^(?P<interface>\d+(\:\d+)?)\s+(\(\d\.\d\))?(?P<chassis_id>\S+)\s+"
        r"(?P<port_id>\S+)\s+\d+\s+\d+",
        re.DOTALL | re.MULTILINE,
    )
    rx_lldp_detail = re.compile(
        r"^\s+- Chassis ID type\s*: (?P<chassis_id_subtype>.+)\n"
        r"^\s+Chassis ID\s*: (?P<chassis_id>\S+)\s*\n"
        r"^\s+- Port ID type\s*: (?P<port_id_subtype>.+)\n"
        r"^\s+Port ID\s*: (?P<port_id>\S+)\s*\n"
        r"^\s+- Time To Live: \d+ seconds\s*\n"
        r"^\s+- System Name: (?P<system_name>.+)\n"
        r"(^\s+- System Description: (?P<system_descr>.+)\n)?"
        r"^\s+- System Capabilities : (?P<system_caps>.+)\n"
        r"^\s+Enabled Capabilities: (?P<enabled_caps>.+)\n"
        r"(^\s+- Port Description: (?P<port_descr>.+)\n)?"
        r"(^\s+- Management Address Subtype:.+)?"
        r"^\s+- IEEE802.3 MAC/PHY Configuration/Status\s*\n",
        re.MULTILINE | re.DOTALL,
    )
    chassis_types = {
        "MAC address (4)": LLDP_CHASSIS_SUBTYPE_MAC,
        "Network address (5); Address type: IPv4 (1)": LLDP_CHASSIS_SUBTYPE_NETWORK_ADDRESS,
        "Locally assigned (7)": LLDP_CHASSIS_SUBTYPE_LOCAL,
    }
    port_types = {
        "MAC address (3)": LLDP_PORT_SUBTYPE_MAC,
        "ifName (5)": LLDP_PORT_SUBTYPE_NAME,
        "Locally assigned (7)": LLDP_PORT_SUBTYPE_LOCAL,
    }

    def execute_cli(self):
        r = defaultdict(list)  # local_iface -> neighbors
        try:
            lldp = self.cli("show lldp neighbors")
        except self.CLISyntaxError:
            raise self.NotSupportedError()
        for match in self.rx_lldp_nei.finditer(lldp):
            local_interface = match.group("interface")
            remote_chassis_id = match.group("chassis_id")
            remote_port = match.group("port_id")

            # Build neighbor data
            # Get capability
            cap = 4
            # Get remote port subtype
            remote_port_subtype = LLDP_PORT_SUBTYPE_NAME
            if is_ipv4(remote_port):
                # Actually networkAddress(4)
                remote_port_subtype = LLDP_PORT_SUBTYPE_NETWORK_ADDRESS
            elif is_mac(remote_port):
                # Actually macAddress(3)
                # Convert MAC to common form
                remote_port = MACAddressParameter().clean(remote_port)
                remote_port_subtype = LLDP_PORT_SUBTYPE_MAC
            elif is_int(remote_port):
                # Actually local(7)
                remote_port_subtype = LLDP_PORT_SUBTYPE_LOCAL

            n = {
                "remote_chassis_id": remote_chassis_id,
                "remote_port": remote_port,
                "remote_capabilities": cap,
                "remote_port_subtype": remote_port_subtype,
            }
            if is_ipv4(n["remote_chassis_id"]) or is_ipv6(n["remote_chassis_id"]):
                n["remote_chassis_id_subtype"] = LLDP_CHASSIS_SUBTYPE_NETWORK_ADDRESS
            elif is_mac(n["remote_chassis_id"]):
                n["remote_chassis_id_subtype"] = LLDP_CHASSIS_SUBTYPE_MAC
            else:
                n["remote_chassis_id_subtype"] = LLDP_CHASSIS_SUBTYPE_LOCAL
            try:
                c = self.cli("show lldp ports %s neighbors detailed" % local_interface)
                match = self.rx_lldp_detail.search(c)
                if match:
                    port_descr = match.group("port_descr")
                    if port_descr:
                        n["remote_port_description"] = port_descr.replace('"', "").strip()
                        n["remote_port_description"] = re.sub(
                            r"\\\n\s*", "", n["remote_port_description"]
                        )
                    n["remote_system_name"] = match.group("system_name").replace('"', "").strip()
                    n["remote_system_name"] = re.sub(r"\\\n\s*", "", n["remote_system_name"])
                    sys_descr = match.group("system_descr")
                    if sys_descr:
                        n["remote_system_description"] = sys_descr.replace('"', "").strip()
                        n["remote_system_description"] = re.sub(
                            r"\\\n\s*", "", n["remote_system_description"]
                        )
                    n["remote_port_subtype"] = self.port_types[
                        match.group("port_id_subtype").strip()
                    ]
                    n["remote_chassis_id_subtype"] = self.chassis_types[
                        match.group("chassis_id_subtype").strip()
                    ]
            except self.CLISyntaxError:
                pass
            r[local_interface].append(n)
        return [{"local_interface": x, "neighbors": r[x]} for x in r]
