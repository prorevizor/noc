# ----------------------------------------------------------------------
# RegexLabel model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional, List, Set, Iterable
import re
import operator
from threading import Lock

# Third-party modules
from mongoengine.document import Document
from mongoengine.fields import StringField, IntField, BooleanField, ListField
from bson.regex import Regex
import cachetools

# NOC modules
from noc.core.model.decorator import on_save, on_delete, is_document


id_lock = Lock()


@on_save
@on_delete
class RegexpLabel(Document):
    meta = {
        "collection": "regexlabels",
        "strict": False,
        "auto_create_index": False,
    }

    name = StringField(unique=True)
    description = StringField()
    # Regular Expresion
    regexp = StringField(required=True)
    regexp_compiled = StringField(required=False)
    # Set Multiline flag
    flag_multiline = BooleanField(default=False)
    # Set DotAll flag
    flag_dotall = BooleanField(default=False)
    # Set labels if match regex
    labels = ListField(StringField())
    # Allow apply for ManagedObject
    enable_managedobject_name = BooleanField(default=False)
    enable_managedobject_address = BooleanField(default=False)
    enable_managedobject_description = BooleanField(default=False)
    # Allow apply for Interface
    enable_interface_name = BooleanField(default=False)
    enable_interface_description = BooleanField(default=False)

    # Caches
    _name_cache = cachetools.TTLCache(maxsize=1000, ttl=60)
    _rx_compiled_cache = cachetools.TTLCache(maxsize=1000, ttl=60)

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_name_cache"), lock=lambda _: id_lock)
    def get_by_name(cls, name: str) -> Optional["Label"]:
        return Label.objects.filter(name=name).first()

    @cachetools.cachedmethod(operator.attrgetter("_rx_compiled_cache"))
    def get_compiled(self) -> re.compile:
        rx = re.compile(self.regexp)
        if self.flag_multiline:
            rx.flags ^= re.MULTILINE
        if self.flag_dotall:
            rx.flags ^= re.DOTALL
        return rx

    @classmethod
    def get_effective_labels(cls, scope: str, value: str) -> List[str]:
        """
        Выбор регулярных выражение осуществляется по `enable_<scope>`.
        Метод должен кешировать скомпилированную форму регулярок и сам набор регулярок
        """
        labels = []
        for rx in RegexpLabel.objects.filter(**{f"enable_{scope}": True}):
            if rx.get_compiled().match(value):
                labels += rx.labels
        return labels

    def on_save(self):
        self._reset_caches()

    def _reset_caches(self):
        try:
            del self._rx_compiled_cache[self.name]
        except KeyError:
            pass
