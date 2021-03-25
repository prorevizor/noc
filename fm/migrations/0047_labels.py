# ----------------------------------------------------------------------
# Migrate labels
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


from collections import defaultdict

# Third-party modules
from pymongo import InsertOne, UpdateMany, UpdateOne

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):

    TAG_COLLETIONS = [("noc.alarms.active", ""), ("noc.alarms.archived", "")]

    def migrate(self):
        labels = defaultdict(set)  # label: settings
        # Mongo models
        for collection, setting in self.TAG_COLLETIONS:
            coll = self.mongo_db[collection]
            coll.bulk_write(
                [UpdateMany({"tags": {"$exists": True}}, {"$rename": {"tags": "labels"}})]
            )
        # Unset tags
        for collection, setting in self.TAG_COLLETIONS:
            coll.bulk_write([UpdateMany({}, {"$unset": {"tags": 1}})])
