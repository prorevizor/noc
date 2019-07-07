# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Brocade.CER-ADV.add_vlan
# ---------------------------------------------------------------------
# Copyright (C) 2007-2013 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.iaddvlan import IAddVlan


class Script(BaseScript):
    """
    Brocade.CER-ADV.add_vlan
    """

    name = "Brocade.CER-ADV.add_vlan"
    interface = IAddVlan

    def execute(self, vlan_id, name, tagged_ports):
        with self.configure():
            self.cli("vlan %d name %s" % (vlan_id, name))
            if tagged_ports:
                self.cli("tagged " + " ".join(tagged_ports))
            self.cli("exit")
        self.save_config()
        return True
