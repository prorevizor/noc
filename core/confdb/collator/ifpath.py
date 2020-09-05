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
from typing import Tuple, List, Union, Set

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
        # self.paths = defaultdict(lambda: defaultdict(list))
        self.paths = defaultdict(list)

    PROTOCOL_MAPPING = {
        "Et": {
            "1000BASET",
            "1000BASETX",
            "100BASETX",
            "10BASET",
            "TransEth100M",
            "TransEth1G",
            "TransEth10G",
        },  # Ethernet
        "ME": {"100BASETX"},
        "Fa": {"100BASETX", "10BASET", "TransEth100M"},  # FastEthernet
        "Fo": {"TransEth40G"},  # FortyGigabitEthernet
        "Gi": {
            "10BASET",
            "1000BASET",
            "1000BASETX",
            "TransEth100M",
            "TransEth1G",
        },  # GigabitEthernet
        "Te": {"TransEth10G"},  # TenGigabitEthernet
        "XG": {"TransEth1G", "TransEth10G"},
    }

    # TransEth1G,TransEth10G
    def get_protocols(self, if_name: str) -> Set[str]:
        return self.PROTOCOL_MAPPING.get(if_name[:2])

    @staticmethod
    def name_path(
        if_name: str,
    ) -> Tuple[Union[str, None], List[str], Union[str, None]]:
        match = rx_ifname_splitter.match(if_name)
        if not match:
            return None, [], None
        if_type, if_path, if_num = match.groups()
        if if_path:
            if_path = rx_ifpath_splitter.findall(if_name[match.end(1) : match.start(3)])
        return if_type, if_path or [], if_num

    def iter_path_component(self, path) -> str:
        """
        Split PathItem list
        :param path:
        :return:
        """
        if not path:
            return None
        for item in reversed(path):
            _, c_path, c_num = self.name_path(item.connection.name)
            # if len(c_path) >= 2:
            #     # Remove first element
            #     # c_path.pop(0)
            #     # Absolute path
            #     continue
            for cp in c_path:
                if not cp.isdigit():
                    # if not number - skipping (X/1/1)
                    logger.warning("Path component '%s' is not digit. Skipping..", cp)
                    continue
                yield cp
            yield c_num
        if item.object.get_data("stack", "stackable"):
            yield item.object.get_data("stack", "member")

    def collate(self, physical_path, interfaces):
        logger.debug("Check physical path: %s", physical_path)
        if not self.paths:
            # SA interface path map
            for if_name, iface in interfaces.items():
                if iface.type != "physical":
                    # Physical scope
                    continue
                if_type, if_path, if_num = self.name_path(if_name)
                if not if_num and not if_type:
                    logger.warning("Not matched ifpath format ifname")
                    continue
                protocols = self.get_protocols(if_type)
                # self.paths[tuple(if_path) or None][if_num].append((if_type, if_name, protocols))
                self.paths[if_num] += [(tuple(if_path), if_name, protocols)]
            logger.debug("Paths mapping %s", self.paths)
        paths_candidate = []

        if_type, if_path, if_num = self.name_path(physical_path[-1].connection.name)
        if if_num not in self.paths:
            logger.warning("Interface number %s is not in mapping", if_num)
            return None

        if if_path:
            # @todo stack check, perhaps move to other collator
            paths_candidate.append(tuple(if_path))

        candidates = [x for x in self.paths[if_num]]
        for num, step in enumerate(self.iter_path_component(physical_path[:-1]), start=1):
            candidates = list(
                filter(
                    lambda x: (len(x[0]) < num) or (len(x[0]) >= num and x[0][-num] == step),
                    candidates,
                )
            )
        paths_candidate.append(tuple(candidates[0][0]))

        logger.debug(
            "Path candidates: %s, protocols: %s", paths_candidate, physical_path[-1].connection.protocols
        )
        if_proto = set(physical_path[-1].connection.protocols)
        for p, if_name, protocols in self.paths[if_num]:
            if p in paths_candidate:
                if protocols and if_proto - protocols:
                    logger.info("Interface proto not coverage models: %s", if_proto - protocols)
                    continue
                return if_name

        return None
