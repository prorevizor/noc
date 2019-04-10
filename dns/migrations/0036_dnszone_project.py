# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# dns project
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Third-party modules
from django.db import models
from south.db import db


class Migration(object):
    depends_on = (("project", "0001_initial"),)

    def forwards(self):
        # Create .state
        Project = db.mock_model(
            model_name="Project",
            db_table="project_project",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )
        db.add_column(
            "dns_dnszone", "project",
            models.ForeignKey(Project, verbose_name="Project", null=True, blank=True)
        )

    def backwards(self):
        db.drop_column("dns_dnszone", "project_id")
