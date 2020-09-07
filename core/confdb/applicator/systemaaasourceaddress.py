# ----------------------------------------------------------------------
# DefaultAAASourceAddressApplicator
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from .query import QueryApplicator


class DefaultAAASourceAddressApplicator(QueryApplicator):
    """
    Apply source-ip
    """

    CHECK_QUERY = "Match('hints', 'system', 'aaa', 'default-ip')"
    QUERY = [
        "Match('hints', 'system', 'aaa', 'default-ip', source) and "
        # Filter all local aaa configs
        "NotMatch('system', 'aaa', 'service', X, 'type', 'local') and "
        # Get all aaa config without source-ip
        "NotMatch('system', 'aaa', 'service', X, 'source-ip') and "
        # Set aaa default source-ip
        "Fact('system', 'aaa', 'service', X, 'source-ip', source)"
    ]
