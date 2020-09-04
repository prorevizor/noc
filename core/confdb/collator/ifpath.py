# ----------------------------------------------------------------------
# IfPathCollator
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import re
from collections import defaultdict
import logging

# NOC modules
from .base import BaseCollator
from typing import Tuple, List, Union

IFTYPE_SPLITTER = " "
IFPATH_SPLITTER = "/"

rx_iftype_detect = re.compile(r"([a-zA-Z_]+)(\d+)")

rx_ifname_splitter = re.compile(r"^(\d*\D+)??(\d+[/:])*(\d+)$")
rx_ifpath_splitter = re.compile(r"(\d+)")

logger = logging.getLogger(__name__)


class IfPathCollator(BaseCollator):
    """
    Direct map between connection name and interface name
    """

    def __init__(self):
        super().__init__()
        self.paths = defaultdict(lambda: defaultdict(list))
        self.paths2 = defaultdict(list)

    PROTOCOL_MAPPING = {
        "Et": {"physical"},  # Ethernet
        "Fa": {"100BASETX", "10BASET"},  # FastEthernet
        "Fo": {},  # FortyGigabitEthernet
        "Gi": {"1000BASET", "1000BASETX"},  # GigabitEthernet
        "Te": {"TransEth1G", "TransEth10G"},  # TenGigabitEthernet
        "XG": {"TransEth1G", "TransEth10G"},
    }

    # TransEth1G,TransEth10G
    def get_protocols(self, if_name):
        return self.PROTOCOL_MAPPING.get(if_name[:2])

    @staticmethod
    def name_path(if_name: str) -> Tuple[Union[str, None], Union[List[str], None], Union[str, None]]:
        match = rx_ifname_splitter.match(if_name)
        if not match:
            return None, [], None
        if_type, if_path, if_num = match.groups()
        if if_path:
            if_path = rx_ifpath_splitter.findall(if_name[match.end(1):match.start(3)])
            # r += ifpath[:-1].split("/")
        return if_type, if_path or [], if_num

    def iter_physical_path(self, path):
        for item in reversed(path):
            _, c_path, c_num = self.name_path(item.connection.name)
            # if len(c_path) >= 2:
            #     # Remove first element
            #     # c_path.pop(0)
            #     # Absolute path
            #     continue
            # @todo if not number - skipping (X/1/1)
            for cp in c_path:
                yield cp
            yield c_num
        if path:
            if item.object.get_data("stack", "stackable"):
                yield item.object.get_data("stack", "member")

    def collate(self, physical_path, interfaces):
        if not self.paths:
            # Interface name
            for if_name, iface in interfaces.items():
                if iface.type != "physical":
                    # Physical scope
                    continue
                if_type, if_path, if_num = self.name_path(if_name)
                if not if_num and not if_type:
                    print("Not matched ifpath format ifname")
                    continue
                protocols = self.get_protocols(if_type)
                self.paths[tuple(if_path) or None][if_num].append((if_type, if_name, protocols))
                self.paths2[if_num] += [(tuple(if_path), if_name, protocols)]
            logger.info("Paths mapping %s", self.paths)
            logger.info("Paths mapping 2 %s", self.paths2)
        paths_candidate = []

        if_type, if_path, if_num = self.name_path(physical_path[-1].connection.name)
        if if_num not in self.paths2:
            logger.warning("Interface number %s is not found", if_num)
            return None
        logger.debug("Physical path", list(self.iter_physical_path(physical_path)))
        if if_path:
            # @todo stack check
            paths_candidate.append(tuple(if_path))

        candidates = [x[0] for x in self.paths2[if_num]]
        for num, step in enumerate(self.iter_physical_path(physical_path[:-1]), start=1):
            candidates = list(filter(lambda x: (len(x) < num) or (len(x) >= num and x[-num] == step), candidates))
        logger.debug("Candidates", candidates)
        paths_candidate.append(tuple(candidates[0]))

        logger.debug("Path candidates", paths_candidate)
        for p, if_name, protocols in self.paths2[if_num]:
            print(p, ":", if_name, protocols)
            if p in paths_candidate:
                return if_name

        print(physical_path, ":", if_type, if_path, if_num)
        return None
