# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# event correlation rule
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db
from django.db import models


class Migration(object):
    def forwards(self):

        # Model 'EventCorrelationRule'
        db.create_table(
            'fm_eventcorrelationrule', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField("Name", max_length=64, unique=True)), ('rule', models.TextField("Rule")),
                ('description', models.TextField("Description", null=True, blank=True)),
                ('is_builtin', models.BooleanField("Is Builtin", default=False))
            )
        )

        db.send_create_signal('fm', ['EventCorrelationRule'])

    def backwards(self):
        db.delete_table('fm_eventcorrelationrule')
