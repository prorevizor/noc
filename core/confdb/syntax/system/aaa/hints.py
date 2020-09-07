# ----------------------------------------------------------------------
# ConfDB hints system aaa
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from ...defs import DEF
from ...patterns import IF_NAME, IP_ADDRESS

HINTS_SYSTEM_AAA = DEF(
    "aaa",
    [
        DEF(
            "default-address", [DEF(IP_ADDRESS, name="ip", gen="make_system_aaa_default_address")],
        ),
        DEF(
            "default-interface",
            [DEF(IF_NAME, name="interface", gen="make_system_aaa_default_interface")],
        ),
    ],
)
