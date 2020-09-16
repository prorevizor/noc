# ----------------------------------------------------------------------
# DefaultAAASourceAddressApplicator
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from .query import QueryApplicator


class DefaultAAASourceAddressLookupApplicator(QueryApplicator):
    """
    Apply source-ip if default-interface set
    """

    CHECK_QUERY = (
        "NotMatch('hints', 'system', 'aaa', 'service-type', stype, 'default-address') and"
        " Match('hints', 'system', 'aaa', 'service-type', stype, 'default-interface')"
    )
    QUERY = [
        # Getting source-ip from default-interface or default-address
        "((Match('hints', 'system', 'aaa', 'service-type', stype, 'default-interface', interface) and "
        " Match('virtual-router', VR, 'forwarding-instance', FI, 'interfaces', interface, 'unit', unit, 'inet', 'address', source)) and "
        " Fact('hints', 'system', 'aaa', 'service-type', stype, 'default-address', source))"
    ]
