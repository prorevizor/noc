# ----------------------------------------------------------------------
# Managed Object loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.main.models.pool import Pool
from noc.sa.models.managedobject import ManagedObject as ManagedObjectModel
from noc.sa.models.profile import Profile
from .base import BaseLoader
from ..models.managedobject import ManagedObject
from noc.core.validators import is_ipv4


class ManagedObjectLoader(BaseLoader):
    """
    Managed Object loader
    """

    name = "managedobject"
    model = ManagedObjectModel
    data_model = ManagedObject

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pools = {p.name: p for p in Pool.objects.all()}

    def clean(self, row):
        """
        Fix pool
        """
        v = super().clean(row)
        v["pool"] = self.pools[v["pool"]]
        v["fm_pool"] = self.pools[v["fm_pool"]] if v["fm_pool"] else v["pool"]
        if "tags" in v:
            v["tags"] = (
                [x.strip().strip('"') for x in v["tags"].split(",") if x.strip()]
                if v["tags"]
                else []
            )
        assert is_ipv4(v["address"])
        v["address"] = v["address"].strip()
        v["profile"] = Profile.get_by_name(v["profile"])
        v["static_client_groups"] = [v["static_client_groups"]] if v["static_client_groups"] else []
        v["static_service_groups"] = (
            [v["static_service_groups"]] if v["static_service_groups"] else []
        )
        return v

    def purge(self):
        """
        Perform pending deletes
        """
        for r_id, msg in reversed(self.pending_deletes):
            self.logger.debug("Deactivating: %s", msg)
            self.c_delete += 1
            try:
                obj = self.model.objects.get(pk=self.mappings[r_id])
                obj.is_managed = False
                obj.container = None
                obj.tags += ["remote:deleted"]
                obj.save()
            except self.model.DoesNotExist:
                pass  # Already deleted
        self.pending_deletes = []
