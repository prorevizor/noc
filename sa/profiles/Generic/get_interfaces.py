# ---------------------------------------------------------------------
# Generic.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from typing import Dict, Optional, Union, Iterable, Tuple, Callable, List, Any
from collections import defaultdict
from itertools import compress, chain

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
from noc.core.mib import mib
from noc.core.ip import IPv4
from noc.core.snmp.render import render_bin
from noc.core.comp import smart_text


class Script(BaseScript):
    name = "Generic.get_interfaces"
    interface = IGetInterfaces
    MAX_REPETITIONS = 30
    MAX_GETNEXT_RETIRES = 1
    MAX_TIMEOUT = 20

    # SNMP_NAME_TABLE = "IF-MIB::ifDescr"
    # SNMP_MAC_TABLE = "IF-MIB::ifPhysAddress"
    SNMP_ADMIN_STATUS_TABLE = "IF-MIB::ifAdminStatus"
    SNMP_OPER_STATUS_TABLE = "IF-MIB::ifOperStatus"
    SNMP_IF_DESCR_TABLE = "IF-MIB::ifAlias"

    INTERFACE_TYPES = {
        1: "other",
        6: "physical",  # ethernetCsmacd
        23: "tunnel",  # ppp
        24: "loopback",  # softwareLoopback
        117: "physical",  # gigabitEthernet
        131: "tunnel",  # tunnel
        135: "SVI",  # l2vlan
        161: "aggregated",  # ieee8023adLag
        53: "SVI",  # propVirtual
    }

    INTERFACE_NAMES = set()

    def get_interface_snmp_type(self, snmp_type):
        return self.INTERFACE_TYPES.get(snmp_type, "unknown")

    def get_bridge_ifindex_mappings(self) -> Dict[int, int]:
        """
        Getting mappings for bridge port number -> ifindex
        :return:
        """
        pid_ifindex_mappings = {}
        for oid, v in self.snmp.getnext(
            mib["BRIDGE-MIB::dot1dBasePortIfIndex"],
            max_repetitions=self.get_max_repetitions(),
            max_retries=self.get_getnext_retires(),
            timeout=self.get_snmp_timeout(),
        ):
            pid_ifindex_mappings[oid.split(".")[-1]] = v
        return pid_ifindex_mappings

    def get_switchport(self) -> Dict[int, Dict[str, Union[int, list]]]:
        result = defaultdict(lambda: {"tagged_vlans": [], "untagged_vlan": None})
        pid_ifindex_mappings = self.get_bridge_ifindex_mappings()
        iface_list = sorted(pid_ifindex_mappings, key=int)
        for oid, pvid in self.snmp.getnext(
            mib["Q-BRIDGE-MIB::dot1qPvid"],
            max_repetitions=self.get_max_repetitions(),
            max_retries=self.get_getnext_retires(),
            timeout=self.get_snmp_timeout(),
        ):
            if not pvid:
                # if pvid is 0
                continue
            o = oid.split(".")[-1]
            result[pid_ifindex_mappings[o]]["untagged_vlan"] = pvid
        for oid, ports_mask in self.snmp.getnext(
            mib["Q-BRIDGE-MIB::dot1qVlanCurrentEgressPorts"],
            max_repetitions=self.get_max_repetitions(),
            max_retries=self.get_getnext_retires(),
            display_hints={mib["Q-BRIDGE-MIB::dot1qVlanCurrentEgressPorts"]: render_bin},
            timeout=self.get_snmp_timeout(),
        ):
            vlan_num = int(oid.split(".")[-1])
            # Getting port as mask,  convert to vlan: Iface list
            for o in compress(
                iface_list,
                [
                    int(x)
                    for x in chain.from_iterable("{0:08b}".format(mask) for mask in ports_mask)
                ],
            ):
                if vlan_num == result[pid_ifindex_mappings[o]]["untagged_vlan"]:
                    # Perhaps port is switchport @todo getting port type
                    continue
                result[pid_ifindex_mappings[o]]["tagged_vlans"] += [vlan_num]
        return result

    def get_portchannels(self) -> Dict[int, int]:
        r = {}
        for ifindex, sel_pc, att_pc in self.snmp.get_tables(
            [
                mib["IEEE8023-LAG-MIB::dot3adAggPortSelectedAggID"],
                mib["IEEE8023-LAG-MIB::dot3adAggPortAttachedAggID"],
            ]
        ):
            if att_pc:
                if sel_pc > 0:
                    r[int(ifindex)] = int(att_pc)
        return r

    def get_enabled_proto(self):
        return {}

    def get_ip_ifaces(self) -> Dict[int, List[Tuple[str, str]]]:
        r = {}
        ip_mask = {}
        for oid, mask in self.snmp.getnext(
            mib["RFC1213-MIB::ipAdEntNetMask"],
            max_repetitions=self.get_max_repetitions(),
            max_retries=self.get_getnext_retires(),
        ):
            address = oid.split(mib["RFC1213-MIB::ipAdEntNetMask"])[-1].strip(".")
            ip_mask[address] = [(address, mask)]
        for oid, ifindex in self.snmp.getnext(
            mib["RFC1213-MIB::ipAdEntIfIndex"],
            max_repetitions=self.get_max_repetitions(),
            max_retries=self.get_getnext_retires(),
        ):
            address = oid.split(mib["RFC1213-MIB::ipAdEntIfIndex"])[-1].strip(".")
            r[ifindex] = ip_mask[address]
        return r

    def filter_interface(self, ifindex: int, name: str) -> bool:
        """
        Filter interface
        :param ifindex:
        :param name:
        :return:
        """
        return True

    def execute_snmp(self, **kwargs):
        ifaces = {}
        subifaces = {}
        switchports = self.get_switchport()
        portchannels = self.get_portchannels()
        self.logger.info("Portchannel %s", portchannels)
        ips = self.get_ip_ifaces()

        # Getting initial iface info, filter result if needed
        for iface in self.scripts.get_interface_properties(
            enable_ifindex=True, enable_interface_mac=True,
        ):
            if not self.filter_interface(iface["ifindex"], iface["interface"]):
                continue
            if "." in iface["interface"]:
                subifaces[iface["ifindex"]] = {
                    "name": iface["interface"],
                    "ifindex": iface["ifindex"],
                    "type": "SVI",
                }
                if "mac" in iface:
                    subifaces[iface["ifindex"]]["mac"] = iface["mac"]
            else:
                ifaces[iface["ifindex"]] = {
                    "name": iface["interface"],
                    "ifindex": iface["ifindex"],
                    "enabled_protocols": [],
                    "subinterfaces": [],
                }
                if "mac" in iface:
                    ifaces[iface["ifindex"]]["mac"] = iface["mac"]
        # Fill interface info
        iter_tables = []
        iter_tables += [
            self.iter_iftable(
                "admin_status",
                self.SNMP_ADMIN_STATUS_TABLE,
                ifindexes=ifaces,
                clean=self.clean_status,
            )
        ]
        iter_tables += [
            self.iter_iftable(
                "oper_status",
                self.SNMP_OPER_STATUS_TABLE,
                ifindexes=ifaces,
                clean=self.clean_status,
            )
        ]
        iter_tables += [
            self.iter_iftable(
                "description",
                self.SNMP_IF_DESCR_TABLE,
                ifindexes=chain(ifaces, subifaces),
                clean=self.clean_ifdescription,
            )
        ]
        iter_tables += [
            self.iter_iftable("mtu", "IF-MIB::ifMtu", ifindexes=chain(ifaces, subifaces))
        ]
        # Collect and merge results
        data = self.merge_tables(*tuple(iter_tables))
        if not ifaces:
            # If empty result - raise error
            raise NotImplementedError
        # Format result
        r = {}
        for ifindex, iface in ifaces.items():
            if ifindex in data:
                iface.update(data[ifindex])
            iface["type"] = self.clean_iftype(iface["name"], ifindex)
            if not iface["type"]:
                self.logger.error("Unknown type for interface %s", iface["name"])
                continue
            if ifindex in ips:
                iface["subinterfaces"] += [
                    {
                        "name": iface["name"],
                        "enabled_afi": ["IPv4"],
                        "ipv4_addresses": [IPv4(*i) for i in ips[iface["ifindex"]]],
                    }
                ]
            if ifindex in switchports:
                sub = {
                    "name": iface["name"],
                    "enabled_afi": ["BRIDGE"],
                }
                sub.update(switchports[iface["ifindex"]])
                iface["subinterfaces"] += [sub]
            if ifindex in portchannels:
                iface["aggregated_interface"] = ifaces[portchannels[ifindex]]["name"]
                iface["enabled_protocols"] = ["LACP"]
            r[iface["name"]] = iface
            # print(switchports[iface["ifindex"]])
        # Proccessed subinterfaces
        for ifindex, sub in subifaces.items():
            ifname, num = sub["name"].split(".", 1)
            if ifname not in r:
                self.logger.info("Sub %s for ignored iface %s", sub["name"], ifname)
                continue
            if ifindex in data:
                sub.update(data[ifindex])
            if ifindex in ips:
                sub["enabled_afi"] = ["IPv4"]
                sub["ipv4_addresses"] = [IPv4(*i) for i in ips[ifindex]]
            if num.isdigit():
                vlan_ids = int(sub["name"].rsplit(".", 1)[-1])
                if 1 <= vlan_ids < 4095:
                    sub["vlan_ids"] = vlan_ids
            r[ifname]["subinterfaces"] += [sub]
        return [{"interfaces": r.values()}]

    def merge_tables(
        self, *args: Optional[Iterable]
    ) -> Dict[int, Dict[str, Union[int, bool, str]]]:
        """
        Merge iterables into single table

        :param args:
        :return:
        """
        r = {}
        for iter_table in args:
            for key, ifindex, value in iter_table:
                if ifindex not in r:
                    r[ifindex] = {"ifindex": ifindex}
                r[ifindex][key] = value
        return r

    @staticmethod
    def clean_default(v):
        return v

    @staticmethod
    def clean_status(v):
        return v == 1

    def clean_ifname(self, v):
        return self.profile.convert_interface_name(v)

    # if ascii or rus text in description
    def clean_ifdescription(self, desc):
        if desc:
            return smart_text(desc, errors="replace")
        return desc

    def clean_iftype(self, ifname: str, ifindex: Optional[int] = None) -> str:
        return self.profile.get_interface_type(ifname)

    def iter_iftable(
        self,
        key: str,
        oid: str,
        ifindexes: Optional[Union[List[int], Dict[int, Any]]] = None,
        clean: Callable = None,
    ) -> Iterable[Tuple[str, Union[str, int]]]:
        """
        Collect part of IF-MIB table.

        :param key:
        :param oid: Base oid, either in numeric or symbolic form
        :param ifindexes: Collect information for single interface only, if set
        :param clean: Cleaning function
        :return:
        """
        clean = clean or self.clean_default
        # Partial
        if ifindexes:
            for r_oid, v in self.snmp.get_chunked(
                [mib[oid, i] for i in ifindexes], timeout_limits=self.get_snmp_timeout()
            ).items():
                try:
                    yield key, int(r_oid.rsplit(".", 1)[1]), clean(v)
                except ValueError:
                    pass
        else:
            # All interfaces
            if "::" in oid:
                oid = mib[oid]
            for r_oid, v in self.snmp.getnext(
                oid,
                max_repetitions=self.get_max_repetitions(),
                max_retries=self.get_getnext_retires(),
            ):
                try:
                    yield key, int(r_oid.rsplit(".", 1)[1]), clean(v)
                except ValueError:
                    pass

    def get_max_repetitions(self):
        return self.MAX_REPETITIONS

    def get_getnext_retires(self):
        return self.MAX_GETNEXT_RETIRES

    def get_snmp_timeout(self):
        return self.MAX_GETNEXT_RETIRES

    def get_interface_ifindex(self, name: str) -> int:
        """
        Get ifindex for given interface
        :param name:
        :return:
        """
        for r_oid, v in self.snmp.getnext(
            mib[self.SNMP_NAME_TABLE],
            max_repetitions=self.get_max_repetitions(),
            max_retries=self.get_getnext_retires(),
        ):
            if self.profile.convert_interface_name(v) == name:
                return int(r_oid.rsplit(".", 1)[1])
        raise KeyError

    def iter_interface_ifindex(self, name, ifindex):
        yield "name", ifindex, self.profile.convert_interface_name(name)
