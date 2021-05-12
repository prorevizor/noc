# ----------------------------------------------------------------------
# Dependency operations
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Callable, Union, TypeVar
from http import HTTPStatus

# Third-party modules
from fastapi import HTTPException
from django.db.models import Model
from mongoengine.document import Document

# NOC modules
from noc.models import is_document
from noc.core.validators import is_objectid, is_int

TModel = TypeVar("TModel", bound=Model)
TDoc = TypeVar("TDoc", bound=Document)


class ListOp(object):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def get_transform(self, value) -> Callable:
        def inner(qs):
            return qs

        return inner


class FilterExact(ListOp):
    def get_transform(self, value):
        def inner(qs):
            return qs.filter(**{self.name: value})

        return inner


class RefFilter(ListOp):
    def __init__(self, name: str, model: Union[TModel, TDoc]):
        super().__init__(name)
        self.model = model

    def get_transform(self, value):
        def inner_document(qs):
            if value and not is_objectid(value):
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=f"'{value}' is not a valid ObjectId",
                )
            vv = self.model.get_by_id(value) if value else None
            if value and not vv:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail=f"NotFond {str(self.model)}: {value}"
                )
            return qs.filter(**{self.name: vv})

        def inner_model(qs):
            if value and not is_int(value):
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=f"'{value}' is not a Integer",
                )
            vv = self.model.get_by_id(int(value)) if value else None
            if value and not vv:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail=f"NotFond {str(self.model)}: {value}"
                )
            return qs.filter(**{self.name: vv})

        if is_document(self.model):
            return inner_document
        return inner_model


class FuncFilter(ListOp):
    def __init__(self, name: str, function: Callable):
        super().__init__(name)
        self.function = function

    def get_transform(self, value):
        def inner(qs):
            r = self.function(qs, value)
            if r is not None:
                return r
            return qs

        return inner
