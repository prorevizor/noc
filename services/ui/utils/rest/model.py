# ----------------------------------------------------------------------
# ModelResource API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Any, Optional, Callable, Dict, TypeVar, Generic, List, Iterable
import inspect
from http import HTTPStatus

# Third-party modules
from django.db.models import Model, QuerySet, Field, ForeignKey
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Security

# NOC modules
from noc.aaa.models.user import User
from noc.core.service.deps.user import get_user_scope
from noc.core.model.fields import DocumentReferenceField
from noc.models import get_model
from ...models.label import LabelItem


T = TypeVar("T", bound=Model)
GET = ["GET"]
POST = ["POST"]


class ModelResourceAPI(Generic[T]):
    """
    Generic Django-backed REST api.

    Data can be retrieved using different `views`, each having own Pydantic model.
    Following views are set by default:
    * default - suitable for listing items
    * label - id + label
    * form - editing form.

    `item_to_<view>` methods convert Django models to Pydantic models.
    Add own `item_to_<view>` methods to define own customized views.
    """

    prefix: str
    model: T

    def __init__(self):
        if not getattr(self, "prefix", None):
            raise ValueError("prefix is not set")
        if not getattr(self, "model", None):
            raise ValueError("model is not set")
        self.router = APIRouter()
        self.api_name = self.prefix.split("/")[-1]
        # Setup endpoints
        for name, fn in inspect.getmembers(self):
            if name.startswith("item_to_"):
                self.setup_view(name[8:])
        self.setup_write()

    @classmethod
    def queryset(cls, user: User) -> QuerySet:
        """
        Get django's queryset adjusted to current user
        :param user:
        :return:
        """
        return cls.model.objects

    @classmethod
    def item_to_default(cls, item: T) -> BaseModel:
        """
        Convert model item to response model for view `default`
        :param item:
        :return:
        """
        raise NotImplementedError

    @classmethod
    def item_to_label(cls, item: T) -> LabelItem:
        """
        Convert model item to response model for view `label`
        :param item:
        :return:
        """
        return LabelItem(id=str(item.id), label=str(item))

    @classmethod
    def item_to_form(cls, item: T) -> BaseModel:
        return cls.item_to_default(item)

    def get_scope_read_default(self):
        """
        Returns scope for view access to default view
        :return:
        """
        return f"{self.api_name}:read:default"

    def get_scope_read_label(self):
        """
        Returns scope for view access to label view
        :return:
        """
        return f"{self.api_name}:read:default"

    def get_scope_read(self, view: str) -> str:
        """
        Get read scope for view
        :param view:
        :return:
        """
        return getattr(self, f"get_scope_read_{view}", self.get_scope_read_default)()

    def get_scope_write(self) -> str:
        """
        Get write scope
        :param view:
        :return:
        """
        return f"{self.api_name}:write"

    def get_scope_delete(self) -> str:
        """
        Get delete scope
        :param view:
        :return:
        """
        return f"{self.api_name}:delete"

    def setup_view(self, view: str) -> None:
        def inner_list(user: User = Security(get_user_scope, scopes=[self.get_scope_read(view)])):
            # @todo: Parse offset=, limit=
            # @todo: X-NOC-Total, X-NOC-Offset, X-NOC-Limit
            return [fmt(item) for item in self.queryset(user).all()]

        def inner_get(
            id: str, user: User = Security(get_user_scope, scopes=[self.get_scope_read(view)])
        ):
            item = self.queryset(user).filter(pk=id).first()
            if not item:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
            return fmt(item)

        def iter_list_paths() -> Iterable[str]:
            if view == "default":
                yield self.prefix
            yield f"{self.prefix}/v/{view}"

        def iter_get_paths() -> Iterable[str]:
            if view == "default":
                yield f"{self.prefix}/{{id}}"
            yield f"{self.prefix}/{{id}}/v/{view}"

        fmt = getattr(self, f"item_to_{view}", None)
        if not fmt:
            raise ValueError(f"item_to_{view} is not defined")
        sig = inspect.signature(fmt)
        if sig.return_annotation is BaseModel:
            raise ValueError(f"item_to_{view} has incorrect return type annotation")
        # List
        for path in iter_list_paths():
            # List
            self.router.add_api_route(
                path=path,
                endpoint=inner_list,
                methods=GET,
                response_model=List[sig.return_annotation],
                tags=["ui"],
                name=f"{self.api_name}_list_{view}",
                description=f"List items with {view} view",
            )
        # Get
        for path in iter_get_paths():
            self.router.add_api_route(
                path=path,
                endpoint=inner_get,
                methods=GET,
                response_model=sig.return_annotation,
                tags=["ui"],
                name=f"{self.api_name}_get_{view}",
                description=f"Get item with {view} view",
            )

    def setup_write(self):
        """
        Setup write endpoints
        :return:
        """

        def get_reference(field: Field) -> Optional[Callable]:
            def inner(value: Any) -> Any:
                if not value:
                    return None
                if not isinstance(value, dict):
                    raise ValueError("{field.name} must be dict")
                v = remote.get_by_id(value["id"])
                if not v:
                    raise ValueError("{field.name} invalid reference")
                return v

            remote = None
            if isinstance(field, ForeignKey):
                remote = field.remote_field.model
            elif isinstance(field, DocumentReferenceField):
                remote = field.document
                if isinstance(remote, str):
                    remote = get_model(remote)
            if not remote:
                return None
            if not hasattr(remote, "get_by_id"):
                raise ValueError(
                    f"{self.model.__class__.__name__}.{field.name} references to {remote.__class__.__name__} without get_by_id() method"
                )
            return inner

        def inner_create(user: User = Security(get_user_scope, scopes=[self.get_scope_write()])):
            ...

        # Get form model
        sig = inspect.signature(self.item_to_form)
        pd_model = sig.return_annotation
        if pd_model is BaseModel:
            raise ValueError(f"item_to_form has incorrect return type annotation")
        # Get model references
        refs: Dict[str, Callable] = {}
        for field in self.model._meta.local_fields:
            r = get_reference(field)
            if r:
                refs[field.name] = r
        self.router.add_api_route(
            path=self.prefix,
            endpoint=inner_create,
            methods=POST,
            response_model=sig.return_annotation,
            tags=["ui"],
            name=f"{self.api_name}_create",
            description=f"Create item",
        )
