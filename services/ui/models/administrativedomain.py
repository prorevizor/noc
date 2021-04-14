# ----------------------------------------------------------------------
# DefaultAdministrativeDomainItem
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional, List

# Third-party modules
from pydantic import BaseModel

# NOC modules
from .utils import Reference


class DefaultAdministrativeDomainItem(BaseModel):
    id: str
    name: str
    parent: Optional[Reference]
    description: Optional[str]
    default_pool: Optional[Reference]
    bioseg_floating_name_template: Optional[Reference]
    bioseg_floating_parent_segment: Optional[Reference]
    labels: List[str]
    effective_labels: List[str]
    remote_system: Optional[Reference]
    remote_id: Optional[str]
    bi_id: Optional[int]


class FormAdministrativeDomainItem(BaseModel):
    name: str
    parent: Optional[Reference]
    description: Optional[str]
    default_pool: Optional[Reference]
    bioseg_floating_name_template: Optional[Reference]
    bioseg_floating_parent_segment: Optional[Reference]
    labels: Optional[List[str]]
