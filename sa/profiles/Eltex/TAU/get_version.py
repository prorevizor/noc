# ---------------------------------------------------------------------
# Eltex.TAU.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "Eltex.TAU.get_version"
    interface = IGetVersion
    cache = True
    always_prefer = "S"

    rx_ver = re.compile(
        r"^(?P<platform>\S+)\s*.+\n"
        r"System version:\s+#(?P<sysver>\S+)\n"
        r"\S.+\nFirmware\sversion:\s+(?P<fwver>\S+)",
        re.MULTILINE,
    )
    rx_shell_platform = re.compile(
        r"^Factory type: (?P<platform>\S+)\s*\S*\n" r"^Factory SN:\s+(?P<serial>\S+)", re.MULTILINE
    )
    rx_shell_version = re.compile(r"^#(?P<version>\S+)")
    rx_shell_fwversion = re.compile(r"^cat /tmp/msp_version\n(?P<fwversion>\S+)\[", re.MULTILINE)
    rx_snmp_version = re.compile(r"^#(?P<version>\S+)$")

    def execute_snmp(self):
        platform = self.snmp.get("1.3.6.1.4.1.35265.4.14.0", cached=True)
        v = self.snmp.get("1.3.6.1.4.1.35265.4.5.0", cached=True)
        match = self.rx_snmp_version.search(v)
        version = match.group("version")
        serial = self.snmp.get("1.3.6.1.4.1.35265.4.3.0", cached=True)
        hardware = self.snmp.get("1.3.6.1.4.1.35265.4.12.0", cached=True)
        return {
            "vendor": "Eltex",
            "platform": platform,
            "version": version,
            "attributes": {"FW version": hardware, "Serial Number": serial},
        }

    def execute_cli(self):
        """
        try:
            c = self.cli("system info", cached=True)
        except self.CLISyntaxError:
            c = self.cli("show system", ignore_errors=True, cached=True)
        match = self.rx_ver.search(c)
        if match:
            platform = match.group("platform")
            fwversion = match.group("fwver")
            version = match.group("sysver")
            serial = ""
            with self.profile.shell(self):
                v = self.cli("cat /tmp/factory", cached=True)
                match = self.rx_serial.search(v)
                if match:
                    serial = match.group("serial")
        else:
            platform = "None"
            fwversion = "None"
            version = "None"
            serial = "None"
        """
        v = self.cli("cat /tmp/factory", cached=True)
        match = self.rx_shell_platform.search(v)
        platform = match.group("platform")
        serial = match.group("serial")
        v = self.cli("cat /version", cached=True)
        match = self.rx_shell_version.search(v)
        version = match.group("version")
        v = self.cli("cat /tmp/msp_version\r\r", cached=True)
        match = self.rx_shell_fwversion.search(v)
        fwversion = match.group("fwversion")

        return {
            "vendor": "Eltex",
            "platform": platform,
            "version": version,
            "attributes": {"FW version": fwversion, "Serial Number": serial},
        }
