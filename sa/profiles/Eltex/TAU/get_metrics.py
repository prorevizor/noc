# ----------------------------------------------------------------------
# Eltex.TAU.get_metrics
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.sa.profiles.Generic.get_metrics import Script as GetMetricsScript, metrics


class Script(GetMetricsScript):
    name = "Eltex.TAU.get_metrics"

    def convert_bytes(self, mem):
        if mem[-1] == "M":
            mem = float(mem[:-1]) * 1024 * 1024
        if mem[-1] == "K":
            mem = float(mem[:-1]) * 1024
        return mem

    @metrics(
        ["CPU | Usage"],
        has_capability="SNMP | OID | fxsMonitoring",
        volatile=False,
        access="S",
    )
    def get_cpu_usage(self, metrics):
        cpu_usage = float(self.snmp.get("1.3.6.1.4.1.35265.1.9.8.0", cached=True))
        self.set_metric(
            id=("CPU | Usage", None),
            path=["", "", "", ""],
            value=int(cpu_usage),
            multi=True,
        )

    @metrics(
        ["Disk | Free"],
        has_capability="SNMP | OID | fxsMonitoring",
        volatile=False,
        access="S",
    )
    def get_disc_free(self, metrics):
        v = self.snmp.get("1.3.6.1.4.1.35265.1.9.4.0", cached=True)
        disc_free = self.convert_bytes(v)
        self.set_metric(
            id=("Disk | Free", None),
            path=[""],
            value=int(disc_free),
            multi=True,
        )

    @metrics(
        ["Memory | Free"],
        has_capability="SNMP | OID | fxsMonitoring",
        volatile=False,
        access="S",
    )
    def get_memory_free(self, metrics):
        v = self.snmp.get("1.3.6.1.4.1.35265.1.9.4.0", cached=True)
        mem_free = self.convert_bytes(v)
        self.set_metric(
            id=("Memory | Free", None),
            path=[""],
            value=int(mem_free),
            multi=True,
        )
