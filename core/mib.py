# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# MIB lookup utilities
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import os
import logging
from threading import Lock

# Third-party modules
from typing import Union, Tuple, Dict, Optional, Any, Callable

# NOC modules
from noc.config import config
from noc.core.snmp.util import render_tc
from noc.core.comp import smart_text

logger = logging.getLogger(__name__)


class MIBRegistry(object):
    PATHS = config.get_customized_paths("cmibs")
    load_lock = Lock()

    def __init__(self):
        self.mib = {}  # type: Dict[str, str]
        self.hints = {}
        self.loaded_mibs = set()

    def __getitem__(self, item):
        # type: (Union[str, Tuple[str, int]]) -> str
        def maybe_get(k):
            # type:  (str) -> str
            v = self.mib.get(k)
            if v is not None:
                return v
            # Missed in the MIB or missed MIB
            mib_name = k.split("::", 1)[0]
            if self.is_loaded(mib_name):
                # Missed in the MIB
                raise KeyError(item)
            # Load MIB
            self.load_mib(mib_name)
            # Get or raise KeyError
            return self.mib[k]

        if isinstance(item, str):
            if ":" not in item:
                return item  # No conversion needed
            if "." in item:
                # <name>(.\d)+
                name, rest = item.split(".", 1)
                return maybe_get(name) + "." + rest
            # <name>
            return maybe_get(item)
        # (<name>, int)
        return ".".join([maybe_get(item[0])] + [str(x) for x in item[1:]])

    @staticmethod
    def mib_to_modname(name):
        # type: (str) -> str
        """
        Convert MIB name to module name (without .py)
        :param name: MIB name, like IF-MIB
        :return: Module name, like if_mib
        """
        return name.lower().replace("-", "_")

    def load_mib(self, name):
        # type: (str) -> None
        """
        Load MIB by name

        :param name: MIB name, like IF-MIB
        :return:
        """
        mod_name = self.mib_to_modname(name)
        if name in self.loaded_mibs:
            return
        with self.load_lock:
            if name in self.loaded_mibs:
                return
            for root in self.PATHS:
                if root != "cmibs":
                    # Custom script
                    base_name = os.path.basename(os.path.dirname(root))
                else:
                    # Common script
                    base_name = "noc"
                logger.debug("Loading MIB: %s", name)
                mn = "%s.cmibs.%s" % (base_name, mod_name)
                try:
                    m = __import__(mn, {}, {}, "MIB")
                except ModuleNotFoundError:
                    raise KeyError(name)
                self.mib.update(getattr(m, "MIB"))
                if hasattr(m, "DISPLAY_HINTS"):
                    self.hints.update(m.DISPLAY_HINTS)
                self.loaded_mibs.add(name)

    def is_loaded(self, name):
        # type: (str) -> bool
        """
        Check MIB is loaded
        :param name:
        :return:
        """
        with self.load_lock:
            return name in self.loaded_mibs

    def reset(self):
        # type: () -> None
        """
        Reset MIB cache

        :return:
        """
        with self.load_lock:
            self.mib = {}
            self.loaded_mibs = set()

    @staticmethod
    def longest_match(d, k):
        # type: (Dict[str, Any], str) -> Optional[Any]
        """
        Returns longest match of key `k` in dict `d`
        :param d:
        :param k:
        :return:
        """
        for prefix in d:
            if prefix == k or k.startswith(prefix + "."):
                return d.get(prefix)
        return None

    def render(self, oid, value, display_hints=None):
        # type: (str, bytes, Dict[str, Callable[[str, bytes], Union[str, bytes]]]) -> str
        """
        Apply display-hint
        :return:
        """
        if display_hints:
            hint = self.longest_match(display_hints, oid)
            if hint:
                return hint(oid, value)
        hint = self.longest_match(self.hints, oid)
        if hint:
            return render_tc(value, hint[0], hint[1])
        return smart_text(value, errors="ignore")


# MIB singleton
mib = MIBRegistry()
