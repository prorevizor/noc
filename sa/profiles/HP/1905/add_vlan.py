# ---------------------------------------------------------------------
# HP.1905.add_vlan
# ---------------------------------------------------------------------
# Copyright (C) 2007-2013 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.iaddvlan import IAddVlan


class Script(BaseScript):
    name = "HP.1905.add_vlan"
    interface = IAddVlan

    def execute(self, vlan_id, name, tagged_ports=None):
        tagged_ports = tagged_ports or []
        a = ""
        if not self.scripts.has_vlan(vlan_id=vlan_id):
            a = 1
        if tagged_ports:
            ports = ""
            for port in tagged_ports:
                if ports:
                    ports = ports + "," + port
                else:
                    ports = port
            tagged = ports
