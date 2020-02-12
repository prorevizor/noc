# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Eltex.MES24xx.get_chassis_id
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.sa.profiles.Generic.get_chassis_id import Script as BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID


class Script(BaseScript):
    name = "Eltex.MES24xx.get_chassis_id"
    interface = IGetChassisID
    cache = True

    rx_mac = re.compile(r"^Chassis Id\s+:\s+(?P<mac>\S+)", re.MULTILINE)

    def execute_cli(self, **kwargs):
        match = self.rx_mac.search(self.cli("show lldp local"))
        return {"first_chassis_mac": match.group("mac"), "last_chassis_mac": match.group("mac")}
