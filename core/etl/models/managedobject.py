# ----------------------------------------------------------------------
# ManagedObjectModel
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional, List
from pydantic import IPvAnyAddress

# NOC modules
from .base import BaseModel
from .typing import Reference
from .administrativedomain import AdministrativeDomainModel
from .authprofile import AuthProfileModel
from .container import ContainerModel
from .managedobjectprofile import ManagedObjectProfileModel
from .networksegment import NetworkSegmentModel
from .resourcegroup import ResourceGroupModel
from .ttsystem import TTSystemModel
from .project import ProjectModel


class ManagedObjectModel(BaseModel):
    id: str
    name: str
    is_managed: bool
    container: Reference["ContainerModel"]
    administrative_domain: Reference["AdministrativeDomainModel"]
    pool: str
    fm_pool: Optional[str]
    segment: Reference["NetworkSegmentModel"]
    profile: str
    object_profile: Reference["ManagedObjectProfileModel"]
    static_client_groups: List[Reference["ResourceGroupModel"]]
    static_service_groups: List[Reference["ResourceGroupModel"]]
    scheme: str
    address: IPvAnyAddress
    port: str
    user: Optional[str]
    password: Optional[str]
    super_password: Optional[str]
    snmp_ro: Optional[str]
    description: Optional[str]
    auth_profile: Optional[Reference["AuthProfileModel"]]
    tags: List[str]
    tt_system: Optional[Reference["TTSystemModel"]]
    tt_queue: Optional[str]
    tt_system_id: Optional[str]
    project: Optional[Reference["ProjectModel"]]

    _csv_fields = [
        "id",
        "name",
        "is_managed",
        "container",
        "administrative_domain",
        "pool",
        "fm_pool",
        "segment",
        "profile",
        "object_profile",
        "static_client_groups",
        "static_service_groups",
        "scheme",
        "address",
        "port",
        "user",
        "password",
        "super_password",
        "snmp_ro",
        "description",
        "auth_profile",
        "tags",
        "tt_system",
        "tt_queue",
        "tt_system_id",
        "project",
    ]
