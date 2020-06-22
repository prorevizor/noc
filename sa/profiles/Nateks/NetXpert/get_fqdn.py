# ---------------------------------------------------------------------
# Nateks.netxpert.get_fqdn
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.sa.profiles.Generic.get_fqdn import Script as BaseScript
from noc.sa.interfaces.igetfqdn import IGetFQDN


class Script(BaseScript):
    name = "Nateks.NetXpert.get_fqdn"
    interface = IGetFQDN

    rx_hostname = re.compile(r"(?P<hostname>\S+) uptime is", re.MULTILINE)

    def execute_cli(self):
        v = self.cli("show version")
        match = self.rx_hostname.search(v)
        if match:
            fqdn = match.group("hostname")
            return fqdn
        raise NotImplementedError
