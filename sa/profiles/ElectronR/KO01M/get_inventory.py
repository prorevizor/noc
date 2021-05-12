# ---------------------------------------------------------------------
# ElectronR.KO01M.get_inventory
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.sa.profiles.Generic.get_inventory import Script as BaseScript
from noc.sa.interfaces.igetinventory import IGetInventory


class Script(BaseScript):
    name = "ElectronR.KO01M.get_inventory"
    interface = IGetInventory

    def get_chassis_sensors(self):
        r = [
            # tempIN
            {
                "name": "temp",
                "status": True,
                "description": "Значение температуры с внутреннего датчика",
                "measurement": "Celsius",
                "snmp_oid": "1.3.6.1.4.1.35419.20.1.140.0",
            },
            {
                "name": "Pulse",
                "status": True,
                "description": "Датчик числа импульсов",
                "measurement": "Unknown",
                "snmp_oid": "1.3.6.1.4.1.35419.20.1.160.0",
            },
        ]
        # Optron input for 1 to 6
        for i in range(1, 6):
            mode = self.snmp.get(f"1.3.6.1.4.1.35419.20.1.{110 + i}.0")
            r += [
                {
                    "name": f"in{i}",
                    "status": bool(mode),
                    "description": f"Цифровой вход номер {i}",
                    "measurement": "Unknown",
                    "snmp_oid": f"1.3.6.1.4.1.35419.20.1.{100 + i}.0",
                }
            ]
        return r

    def execute_snmp(self):
        r = self.get_inv_from_version()
        sensors = self.get_chassis_sensors()
        if sensors:
            r[0]["sensors"] = sensors
        return r
