# ---------------------------------------------------------------------
# inv.inv sensor plugin
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from .base import InvPlugin
from noc.inv.models.sensor import Sensor


class SensorPlugin(InvPlugin):
    name = "sensor"
    js = "NOC.inv.inv.plugins.sensor.SensorPanel"
