# ----------------------------------------------------------------------
# Auth Profile Loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from .base import BaseLoader
from ..models.authprofile import AuthProfileModel
from noc.sa.models.authprofile import AuthProfile


class AuthProfileLoader(BaseLoader):
    """
    Managed Object Profile loader
    """

    name = "authprofile"
    model = AuthProfile
    data_model = AuthProfileModel
    fields = [
        "id",
        "name",
        "description",
        "type",
        "user",
        "password",
        "super_password",
        "snmp_ro",
        "snmp_rw",
    ]
