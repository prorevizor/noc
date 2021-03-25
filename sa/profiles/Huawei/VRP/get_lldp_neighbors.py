# ---------------------------------------------------------------------
# Huawei.VRP.get_lldp_neighbors
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.sa.profiles.Generic.get_lldp_neighbors import Script as BaseScript
from noc.sa.interfaces.igetlldpneighbors import IGetLLDPNeighbors, MACAddressParameter
from noc.core.text import parse_kv
from noc.core.lldp import (
    LLDP_CHASSIS_SUBTYPE_MAC,
    LLDP_CHASSIS_SUBTYPE_CHASSIS_COMPONENT,
    LLDP_CHASSIS_SUBTYPE_PORT_COMPONENT,
    LLDP_CHASSIS_SUBTYPE_NETWORK_ADDRESS,
    LLDP_CHASSIS_SUBTYPE_LOCAL,
    LLDP_PORT_SUBTYPE_COMPONENT,
    LLDP_PORT_SUBTYPE_NAME,
    LLDP_PORT_SUBTYPE_ALIAS,
    LLDP_PORT_SUBTYPE_MAC,
    LLDP_PORT_SUBTYPE_NETWORK_ADDRESS,
    LLDP_PORT_SUBTYPE_LOCAL,
    LLDP_CAP_OTHER,
    LLDP_CAP_REPEATER,
    LLDP_CAP_BRIDGE,
    LLDP_CAP_WLAN_ACCESS_POINT,
    LLDP_CAP_ROUTER,
    LLDP_CAP_TELEPHONE,
    LLDP_CAP_DOCSIS_CABLE_DEVICE,
    LLDP_CAP_STATION_ONLY,
    lldp_caps_to_bits,
)


class Script(BaseScript):
    name = "Huawei.VRP.get_lldp_neighbors"
    interface = IGetLLDPNeighbors

    always_prefer = "C"  # For old models, not supported by SNMP

    rx_iface_sep = re.compile(r"^(\S+)\s+has\s+\d+\s+neighbors?", re.MULTILINE)
    rx_iface3_sep = re.compile(
        r"^LLDP neighbor-information of port \d+\[(?P<local_iface>\S+)\]:", re.MULTILINE
    )

    rx_neighbor_split = re.compile(r"^\s*Neighbor", re.MULTILINE)

    CHASSIS_TYPES = {
        "chassiscomponent": LLDP_CHASSIS_SUBTYPE_CHASSIS_COMPONENT,
        "chassis component": LLDP_CHASSIS_SUBTYPE_CHASSIS_COMPONENT,
        "portcomponent": LLDP_CHASSIS_SUBTYPE_PORT_COMPONENT,
        "port component": LLDP_CHASSIS_SUBTYPE_PORT_COMPONENT,
        "macaddress": LLDP_CHASSIS_SUBTYPE_MAC,
        "mac address": LLDP_CHASSIS_SUBTYPE_MAC,
        "networkaddress": LLDP_CHASSIS_SUBTYPE_NETWORK_ADDRESS,
        "network address": LLDP_CHASSIS_SUBTYPE_NETWORK_ADDRESS,
        "interfacename": 6,
        "interface name": 6,
        "local": LLDP_CHASSIS_SUBTYPE_LOCAL,
        "locally assigned": LLDP_CHASSIS_SUBTYPE_LOCAL,
    }

    PORT_TYPES = {
        "interfacealias": LLDP_PORT_SUBTYPE_ALIAS,
        "interface alias": LLDP_PORT_SUBTYPE_ALIAS,
        "portcomponent": LLDP_PORT_SUBTYPE_COMPONENT,
        "port component": LLDP_PORT_SUBTYPE_COMPONENT,
        "macaddress": LLDP_PORT_SUBTYPE_MAC,
        "mac address": LLDP_PORT_SUBTYPE_MAC,
        "interfacename": LLDP_PORT_SUBTYPE_NAME,
        "interface name": LLDP_PORT_SUBTYPE_NAME,
        "local": LLDP_PORT_SUBTYPE_LOCAL,
        "locally assigned": LLDP_PORT_SUBTYPE_LOCAL,
    }

    CAPS = {
        "--": 0,
        "na": 0,
        "other": 1,
        "repeater": 2,
        "bridge": 4,
        "wlan": 8,
        "wlanaccesspoint": 8,
        "access point": 8,
        "router": 16,
        "telephone": 32,
        "cable": 64,
        "docsiscabledevice": 64,
        "station": 128,
        "stationonly": 128,
    }

    def execute_cli(self, **kwargs):
        """
        VRP5 style
        :return:
        """
        r = []
        if self.is_kernel_3:
            try:
                v = self.cli("display lldp neighbor-information")
            except self.CLISyntaxError:
                return []
        else:
            try:
                v = self.cli("display lldp neighbor")
            except self.CLISyntaxError:
                return []
        il = self.rx_iface_sep.split(v)[1:]
        if not il:
            il = self.rx_iface3_sep.split(v)[1:]
        for local_iface, data in zip(il[::2], il[1::2]):
            neighbors = []
            for ndata in self.rx_neighbor_split.split(data)[1:]:
                n = parse_kv(
                    {
                        "chassis type": "remote_chassis_id_subtype",
                        "chassisidsubtype": "remote_chassis_id_subtype",
                        "chassis id": "remote_chassis_id",
                        "chassisid": "remote_chassis_id",
                        "port id type": "remote_port_subtype",
                        "portidsubtype": "remote_port_subtype",
                        "port id subtype": "remote_port_subtype",
                        "port id": "remote_port",
                        "portid": "remote_port",
                        "port description": "remote_port_description",
                        "portdesc": "remote_port_description",
                        "system capabilities enabled": "remote_capabilities",
                        "syscapenabled": "remote_capabilities",
                        "system name": "remote_system_name",
                        "sysname": "remote_system_name",
                        "system description": "remote_system_description",
                        "sysdesc": "remote_system_description",
                    },
                    ndata,
                )
                # Convert chassis id
                n["remote_chassis_id_subtype"] = self.CHASSIS_TYPES[
                    n["remote_chassis_id_subtype"].lower()
                ]
                if n["remote_chassis_id_subtype"] == 3:
                    n["remote_chassis_id"] = MACAddressParameter().clean(n["remote_chassis_id"])
                # Convert port id
                n["remote_port_subtype"] = self.PORT_TYPES[n["remote_port_subtype"].lower()]
                if n["remote_port_subtype"] == 3:
                    n["remote_port"] = MACAddressParameter().clean(n["remote_port"])
                if n.get("remote_port_description") in ["--", "NA", "N/A"]:
                    del n["remote_port_description"]
                if n.get("remote_system_description") in ["--", "NA", "N/A"]:
                    del n["remote_system_description"]
                if n.get("remote_system_name") in ["--", "NA", "N/A"]:
                    del n["remote_system_name"]
                # Process capabilities
                caps = 0
                cs = n.get("remote_capabilities", "").replace(",", " ")
                for c in cs.split():
                    caps |= self.CAPS[c.lower().strip()]
                n["remote_capabilities"] = caps
                neighbors += [n]
            if neighbors:
                r += [{"local_interface": local_iface, "neighbors": neighbors}]
        return r
