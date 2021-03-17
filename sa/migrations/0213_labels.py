# ----------------------------------------------------------------------
# Migrate labels
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


from collections import defaultdict

# Third-party modules
from pymongo import InsertOne, UpdateMany

# NOC modules
from noc.core.migration.base import BaseMigration
from django.contrib.postgres.fields import ArrayField
from django.db.models import CharField


class Migration(BaseMigration):
    def migrate(self):
        labels = defaultdict(set)  # label: setting
        # Create labels fields
        # ManagedObjectProfile
        for table, setting in [
            ("sa_managedobject", "managedobject"),
            ("sa_managedobjectprofile", "managedobjectprofile"),
            ("sa_administrativedomain", "administrativedomain"),
            ("sa_authprofile", "authprofile"),
            ("sa_commandsnippet", "commandsnippet"),
        ]:
            self.db.add_column(
                table,
                "labels",
                ArrayField(CharField(max_length=250), null=True, blank=True, default=lambda: "{}"),
            )
            self.db.add_column(
                table,
                "effective_labels",
                ArrayField(CharField(max_length=250), null=True, blank=True, default=lambda: "{}"),
            )
            # Migrate data
            self.db.execute(
                """
                UPDATE %s
                SET labels = tags
                WHERE tags is not NULL and tags <> '{}'
                """
                % table
            )
            # Fill labels
            for ll in self.db.execute(
                """
                SELECT DISTINCT labels
                FROM %s
                WHERE labels <> '{}'
                """
                % table
            ):
                for name in ll[0]:
                    labels[name].add(f"enable_{setting}")
            # Delete tags
            self.db.delete_column(
                table,
                "tags",
            )
        # Mongo models
        for collection, setting in [
            ("noc.services", "service"),
            ("noc.serviceprofiles", "serviceprofiles"),
        ]:
            coll = self.mongo_db[collection]
            coll.aggregate(
                [
                    {"$match": {"tags": {"$exists": True, "$ne": []}}},
                    {"$addFields": {"labels": "$tags"}},
                    {"$out": collection},
                ]
            )
            r = next(
                coll.aggregate(
                    [
                        {"$match": {"tags": {"$exists": True, "$ne": []}}},
                        {"$unwind": "$labels"},
                        {"$group": {"_id": 1, "all_labels": {"$addToSet": "$labels"}}},
                    ]
                )
            )
            if r:
                for ll in r["all_labels"]:
                    labels[ll].add(f"enable_{setting}")
            # Unset tags
            coll.bulk_write([UpdateMany({}, {"$unseet": "tags"})])
        # Add labels
        self.create_labels(labels)
        # Migrate selector

    def create_labels(self, labels):
        bulk = []
        l_coll = self.mongo_db["labels"]
        for label in labels:
            doc = {
                # "_id": bson.ObjectId(),
                "name": label,
                "description": "",
                "bg_color1": 8359053,
                "bg_color2": 8359053,
                # Label scope
                "enable_agent": False,
                "enable_service": False,
                "enable_serviceprofile": False,
                "enable_managedobject": False,
                "enable_managedobjectprofile": False,
                "enable_administrativedomain": False,
                "enable_authprofile": False,
                "enable_commandsnippet": False,
                # Exposition scope
                "expose_metric": False,
                "expose_managedobject": False,
            }
            for setting in labels[label]:
                doc[setting] = True
            bulk += [InsertOne(doc)]
        if bulk:
            l_coll.bulk_write(bulk, ordered=True)
