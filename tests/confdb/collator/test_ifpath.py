# ----------------------------------------------------------------------
# Run tests over tests/confdb/profiles
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


# Third-party modules
import pytest
from collections import namedtuple

# NOC modules
from noc.core.handler import get_handler


PREFIX = ("tests", "confdb", "profiles")

MOCK1_STACK_DATA = {"stack": {"stackable": True, "member": 1}}

INTERFACES1 = [
    ("GigabitEthernet0/0/1", "physical"),
    ("GigabitEthernet0/0/2", "physical"),
    ("GigabitEthernet0/0/3", "physical"),
    ("GigabitEthernet0/0/4", "physical"),
    ("GigabitEthernet0/0/10", "physical"),
    ("XGigabitEthernet0/1/1", "physical"),
    ("XGigabitEthernet0/1/2", "physical"),
    ("M-Ethernet0/0/1", "physical"),
]

PATHS1 = [
    [
        [
            {"object": ("MockObject1", {}), "connection": ("1", "")},
            {"object": ("Connection1", {}), "connection": ("xfp 1", ["TransEth10G"])},
        ],
        "XGigabitEthernet0/1/1",
    ],
    [
        [
            {"object": ("MockObject1", {}), "connection": ("1", "")},
            {"object": ("Connection1", {}), "connection": ("xfp 2", ["TransEth10G"])},
        ],
        "XGigabitEthernet0/1/2",
    ],
    [
        [{"object": ("MockObject1", {}), "connection": ("MEth0/0/1", ["10BASET", "100BASETX"])}],
        "M-Ethernet0/0/1",
    ],
    [
        [
            {
                "object": ("MockObject1", {}),
                "connection": ("GigabitEthernet0/0/1", ["TransEth100M", "TransEth1G"]),
            }
        ],
        "GigabitEthernet0/0/1",
    ],
    [
        [
            {
                "object": ("MockObject1", {}),
                "connection": ("GigabitEthernet0/0/2", ["TransEth100M", "TransEth1G"]),
            }
        ],
        "GigabitEthernet0/0/2",
    ],
    [
        [
            {
                "object": ("MockObject1", {}),
                "connection": ("GigabitEthernet0/0/3", ["TransEth100M", "TransEth1G"]),
            }
        ],
        "GigabitEthernet0/0/3",
    ],
]

PathItem = namedtuple("PathItem", ["object", "connection"])


class MockObject(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def get_data(self, interface, key):
        pass


class MockObjectConnection(object):
    def __init__(self, name, protocols):
        self.name = name
        self.protocols = protocols


class MockInterface(object):
    def __init__(self, name, default_name, type):
        self.name = name
        self.default_name = default_name
        self.type = type


@pytest.mark.parametrize("interfaces,paths", [(INTERFACES1, PATHS1)])
def test_profile(interfaces, paths):
    ifaces = {}
    for iface_name, iface_type in interfaces:
        ifaces[iface_name] = MockInterface(iface_name, "", iface_type)

    h = get_handler("noc.core.confdb.collator.ifpath.IfPathCollator")
    collator = h()

    for path, result in paths:
        physical_path = [
            PathItem(
                object=MockObject(*p["object"]), connection=MockObjectConnection(*p["connection"])
            )
            for p in path
        ]
        r = collator.collate(physical_path, ifaces)
        assert r == result
