# ----------------------------------------------------------------------
# Eltex.MES.get_metrics
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.sa.profiles.Generic.get_metrics import Script as GetMetricsScript, metrics


class Script(GetMetricsScript):
    name = "Eltex.MES.get_metrics"

    @metrics(
        ["Interface | Tail_Drop"],
        has_capability="SNMP | Bulk",
        matcher="is_3124",
        volatile=False,
        access="S",
    )
    def get_tail_drop_snmp(self, metrics):
        # iso.3.6.1.4.1.35265.1.23.1.8.1.2.1.1.1.5.{ifindex}.{queue}.0
        names = {x: y for y, x in self.scripts.get_ifindexes().items()}
        for oid, v in self.snmp.getnext("1.3.6.1.4.1.35265.1.23.1.8.1.2.1.1.1.5", bulk=False):
            oid2 = oid.split("1.3.6.1.4.1.35265.1.23.1.8.1.2.1.1.1.5.")
            ifindex = oid2[1].split(".")
            if ifindex[2] == "0":
                iface_name = names[int(ifindex[0])]
                queue = int(ifindex[1])
                self.set_metric(
                    id=("Interface | Tail_Drop", None),
                    path=["", "", queue, iface_name],
                    value=int(v),
                    multi=True,
                )
