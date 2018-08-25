# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Alstec.MSPU.get_ifindexes
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.sa.profiles.Generic.get_ifindexes import Script as BaseScript
from noc.sa.interfaces.igetifindexes import IGetIfindexes


class Script(BaseScript):
    name = "Alstec.MSPU.get_ifindexes"
    interface = IGetIfindexes

    INTERFACE_NAME_OID = "IF-MIB::ifName"
