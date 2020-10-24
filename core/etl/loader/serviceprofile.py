# ----------------------------------------------------------------------
# ServiceProfile loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from .base import BaseLoader
from ..models.service import ServiceModel
from noc.sa.models.serviceprofile import ServiceProfile


class ServiceProfileLoader(BaseLoader):
    """
    Service Profile loader
    """

    name = "serviceprofile"
    model = ServiceProfile
    data_model = ServiceModel
    fields = ["id", "name", "description", "card_title_template"]
