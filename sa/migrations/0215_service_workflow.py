# ----------------------------------------------------------------------
# Migrate servie to workflow
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


from bson import ObjectId

# Third-party modules
from pymongo import InsertOne, UpdateMany, UpdateOne

# NOC modules
from noc.core.migration.base import BaseMigration
from django.contrib.postgres.fields import ArrayField
from django.db.models import CharField


class Migration(BaseMigration):
    depends_on = [("wf", "0004_service_default")]

    def migrate(self):
        coll = self.mongo_db["noc.services"]
        coll.bulk_write(
            [
                # "Planned"
                UpdateMany(
                    {"logical_status": "P"},
                    {"$set": {"state": ObjectId("606eb01dd179a5da7e340a43")}},
                ),
                # "Provisioning"
                UpdateMany(
                    {"logical_status": "p"},
                    {"$set": {"state": ObjectId("606eb02ed179a5da7e340a45")}},
                ),
                # "Testing"
                UpdateMany(
                    {"logical_status": "T"},
                    {"$set": {"state": ObjectId("606eb035d179a5da7e340a47")}},
                ),
                # "Ready"
                UpdateMany(
                    {"logical_status": "R"},
                    {"$set": {"state": ObjectId("606eb041d179a5da7e340a49")}},
                ),
                # "Suspended"
                UpdateMany(
                    {"logical_status": "S"},
                    {"$set": {"state": ObjectId("606eb04ed179a5da7e340a4b")}},
                ),
                # "Removing"
                UpdateMany(
                    {"logical_status": "r"},
                    {"$set": {"state": ObjectId("606eb055d179a5da7e340a4d")}},
                ),
                # "Closed"
                UpdateMany(
                    {"logical_status": "C"},
                    {"$set": {"state": ObjectId("606eb05fd179a5da7e340a4f")}},
                ),
                # "Unknown"
                UpdateMany(
                    {"logical_status": "U"},
                    {"$set": {"state": ObjectId("606eaffbd179a5da7e340a41")}},
                ),
                # Rename state_changed
                UpdateMany(
                    {"logical_status_start": {"$exists": True}},
                    {"$rename": {"logical_status_start": "state_changed"}},
                ),
            ]
        )
