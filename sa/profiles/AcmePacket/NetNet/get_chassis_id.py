# ----------------------------------------------------------------------
# AcmePacket.NetNet.get_chassis_id
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.sa.profiles.Generic.get_chassis_id import Script as BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID


class Script(BaseScript):

    name = "AcmePacket.NetNet.get_chassis_id"
    interface = IGetChassisID
