# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Subscriber loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import operator

# Third-party modules
import cachetools

# NOC modules
from .base import BaseLoader
from noc.crm.models.subscriberprofile import SubscriberProfile
from noc.crm.models.subscriber import Subscriber


class SubscriberLoader(BaseLoader):
    """
    Administrative division loader
    """

    name = "subscriber"
    model = Subscriber
    fields = [
        "id",
        "name",
        "description",
        "profile",
        "address",
        "tech_contact_person",
        "tech_contact_phone",
    ]

    mapped_fields = {
        "profile": "subscriberprofile",
    }

    discard_deferred = True

    _profile_cache = {}

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_profile_cache"))
    def get_profile(cls, name):
        return SubscriberProfile.objects.get(name=name)

    # def clean(self, row):
    #     d = super(SubscriberLoader, self).clean(row)
    #     if "profile" in d:
    #         d["profile"] = self.get_profile(d["profile"])
    #     return d

    def find_object(self, v):
        """
        Find object by remote system/remote id
        :param v:
        :return:
        """
        if not v.get("remote_system") or not v.get("remote_id"):
            self.logger.warning("RS or RID not found")
            return None
        if not hasattr(self, "_subscriber_remote_ids"):
            self.logger.info("Filling service collection")
            coll = Subscriber._get_collection()
            self._subscriber_remote_ids = {
                c["remote_id"]: c["_id"]
                for c in coll.find(
                    {"remote_system": v["remote_system"].id, "remote_id": {"$exists": True}},
                    {"remote_id": 1, "_id": 1},
                )
            }
        if v["remote_id"] in self._subscriber_remote_ids:
            return Subscriber.objects.get(id=self._subscriber_remote_ids[v["remote_id"]])
        return None
