# ----------------------------------------------------------------------
# Service
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
import logging
import operator
from threading import Lock
from typing import Any, Dict, Optional

# Third-party modules
from mongoengine.document import Document
from mongoengine.fields import (
    StringField,
    DateTimeField,
    ReferenceField,
    ListField,
    EmbeddedDocumentField,
    LongField,
    ObjectIdField,
)
import cachetools

# NOC modules
from .serviceprofile import ServiceProfile
from noc.crm.models.subscriber import Subscriber
from noc.crm.models.supplier import Supplier
from noc.main.models.remotesystem import RemoteSystem
from noc.core.mongo.fields import ForeignKeyField, PlainReferenceField
from noc.sa.models.managedobject import ManagedObject
from noc.core.bi.decorator import bi_sync
from noc.core.model.decorator import on_save, on_delete, on_delete_check
from noc.core.resourcegroup.decorator import resourcegroup
from noc.wf.models.state import State
from noc.core.wf.decorator import workflow
from noc.inv.models.capsitem import CapsItem
from noc.main.models.label import Label

logger = logging.getLogger(__name__)

id_lock = Lock()


@Label.model
@bi_sync
@on_save
@resourcegroup
@workflow
@on_delete
@on_delete_check(clean=[("phone.PhoneNumber", "service"), ("inv.Interface", "service")])
class Service(Document):
    meta = {
        "collection": "noc.services",
        "strict": False,
        "auto_create_index": False,
        "indexes": [
            "subscriber",
            "supplier",
            "managed_object",
            "parent",
            "order_id",
            "static_service_groups",
            "effective_service_groups",
            "static_client_groups",
            "effective_client_groups",
        ],
    }
    profile = ReferenceField(ServiceProfile, required=True)
    # Creation timestamp
    ts = DateTimeField(default=datetime.datetime.now)
    # Logical state of service
    state = PlainReferenceField(State)
    # Last state change
    state_changed = DateTimeField()
    # Parent service
    parent = ReferenceField("self", required=False)
    # Subscriber information
    subscriber = ReferenceField(Subscriber)
    # Supplier information
    supplier = ReferenceField(Supplier)
    description = StringField()
    #
    agreement_id = StringField()
    # Order Fulfillment order id
    order_id = StringField()
    stage_id = StringField()
    stage_name = StringField()
    stage_start = DateTimeField()
    # Billing contract number
    account_id = StringField()
    # Connection address
    address = StringField()
    # For port services
    managed_object = ForeignKeyField(ManagedObject)
    # NRI port id, converted by portmapper to native name
    nri_port = StringField()
    # CPE information
    cpe_serial = StringField()
    cpe_mac = StringField()
    cpe_model = StringField()
    cpe_group = StringField()
    # Capabilities
    caps = ListField(EmbeddedDocumentField(CapsItem))
    # Integration with external NRI and TT systems
    # Reference to remote system object has been imported from
    remote_system = ReferenceField(RemoteSystem)
    # Object id in remote system
    remote_id = StringField()
    # Object id in BI
    bi_id = LongField(unique=True)
    # Labels
    labels = ListField(StringField())
    effective_labels = ListField(StringField())
    # Resource groups
    static_service_groups = ListField(ObjectIdField())
    effective_service_groups = ListField(ObjectIdField())
    static_client_groups = ListField(ObjectIdField())
    effective_client_groups = ListField(ObjectIdField())

    _id_cache = cachetools.TTLCache(maxsize=100, ttl=60)

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id) -> Optional["Service"]:
        return Service.objects.filter(id=id).first()

    def __str__(self):
        return str(self.id) if self.id else "new service"

    def on_delete(self):
        if self.nri_port:
            self.unbind_interface()

    def on_save(self):
        if not hasattr(self, "_changed_fields") or "nri_port" in self._changed_fields:
            self.unbind_interface()
        if not hasattr(self, "_changed_fields") or "parent" in self._changed_fields:
            self._refresh_managed_object()

    def _refresh_managed_object(self):
        from noc.sa.models.servicesummary import ServiceSummary

        mo = self.get_managed_object()
        if mo:
            ServiceSummary.refresh_object(mo)

    def unbind_interface(self):
        from noc.inv.models.interface import Interface

        Interface._get_collection().update({"service": self.id}, {"$unset": {"service": ""}})
        self._refresh_managed_object()

    def get_managed_object(self):
        r = self
        while r:
            if r.managed_object:
                return self.managed_object
            r = r.parent
        return None

    def get_caps(self) -> Dict[str, Any]:
        return CapsItem.get_caps(self.caps, self.profile.caps)

    @classmethod
    def can_set_label(cls, label):
        return Label.get_effective_setting(label, "enable_service")
