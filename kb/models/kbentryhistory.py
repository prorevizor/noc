# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# KBEntryHistory model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from django.db import models
# NOC modules
from noc.core.model.base import NOCModel
from noc.aaa.models.user import User
from noc.kb.models.kbentry import KBEntry


class KBEntryHistory(NOCModel):
    """
    Modification History
    """
    class Meta:
        verbose_name = "KB Entry History"
        verbose_name_plural = "KB Entry Histories"
        app_label = "kb"
        db_table = "kb_kbentryhistory"
        ordering = ("kb_entry", "timestamp")

    kb_entry = models.ForeignKey(KBEntry, verbose_name="KB Entry")
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)
    user = models.ForeignKey(User, verbose_name="User")
    diff = models.TextField("Diff")
