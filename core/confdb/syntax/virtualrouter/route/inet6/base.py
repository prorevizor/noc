# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ConfDB virtual router <name> route inet6 syntax
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# NOC modules
from ....defs import DEF
from ....patterns import IPv4_PREFIX, IPv6_ADDRESS

VR_ROUTE_INET6_SYNTAX = DEF(
    "inet6",
    [
        DEF(
            "static",
            [
                DEF(
                    IPv4_PREFIX,
                    [
                        DEF(
                            "next-hop",
                            [
                                DEF(
                                    IPv6_ADDRESS,
                                    multi=True,
                                    name="next_hop",
                                    gen="make_inet6_static_route_next_hop",
                                )
                            ],
                        )
                    ],
                )
            ],
        )
    ],
)
