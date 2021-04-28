# ---------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import os
import threading
import operator

# Third-party modules
from mongoengine.document import Document
from mongoengine.fields import StringField, LongField, UUIDField
import cachetools

# NOC modules
from noc.core.bi.decorator import bi_sync
from noc.core.prettyjson import to_json
from noc.core.model.decorator import on_delete_check
from noc.core.profile.loader import loader, GENERIC_PROFILE

id_lock = threading.Lock()


@bi_sync
@on_delete_check(
    check=[
        ("inv.Firmware", "profile"),
        ("sa.ActionCommands", "profile"),
        ("sa.ManagedObject", "profile"),
        ("sa.ManagedObjectSelector", "filter_profile"),
        ("sa.ProfileCheckRule", "profile"),
        ("dev.Spec", "profile"),
        ("peer.PeeringPoint", "profile"),
    ]
)
class Profile(Document):
    meta = {
        "collection": "noc.profiles",
        "strict": False,
        "auto_create_index": False,
        "json_collection": "sa.profiles",
        "json_unique_fields": ["name"],
    }
    name = StringField(unique=True)
    description = StringField(required=False)
    # Global ID
    uuid = UUIDField(binary=True)
    # Object id in BI
    bi_id = LongField(unique=True)

    _id_cache = cachetools.TTLCache(1000, ttl=60)
    _bi_id_cache = cachetools.TTLCache(1000, ttl=60)
    _name_cache = cachetools.TTLCache(1000, ttl=60)

    def __str__(self):
        return self.name

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id):
        return Profile.objects.filter(id=id).first()

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_bi_id_cache"), lock=lambda _: id_lock)
    def get_by_bi_id(cls, id):
        return Profile.objects.filter(bi_id=id).first()

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_name_cache"), lock=lambda _: id_lock)
    def get_by_name(cls, name):
        return Profile.objects.filter(name=name).first()

    def to_json(self):
        return to_json(
            {
                "$collection": self._meta["json_collection"],
                "name": self.name,
                "uuid": self.uuid,
                "description": self.description,
            },
            order=["name", "uuid", "description"],
        )

    def get_json_path(self):
        vendor, soft = self.name.split(".")
        return os.path.join(vendor, "%s.json" % soft)

    def get_profile(self):
        return loader.get_profile(self.name)()

    @property
    def is_generic(self):
        return self.name == GENERIC_PROFILE

    @classmethod
    def get_generic_profile_id(cls):
        if not hasattr(cls, "_generic_profile_id"):
            cls._generic_profile_id = Profile.objects.filter(name=GENERIC_PROFILE).first().id
        return cls._generic_profile_id

    @classmethod
    def iter_lazy_labels(cls, profile: "Profile"):
        yield f"noc::profile::{profile.name}::="
