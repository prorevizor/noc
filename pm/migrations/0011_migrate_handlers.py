# ---------------------------------------------------------------------
# Change ThresholdProfiles handlers
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
import bson

# NOC modules
from noc.core.migration.base import BaseMigration

HTYPE = {
    "umbrella_filter_handler": "allow_threshold_handler",
    "value_handler": "allow_threshold_value_handler",
}


class Migration(BaseMigration):
    def migrate(self):
        # Create handlers
        self.migrate_create_handlers()
        # Change handlers
        self.migrate_change_handlers()

    def migrate_create_handlers(self):
        h_coll = self.mongo_db["handlers"]
        thp_handlers = {}
        thps = self.mongo_db["thresholdprofiles"]
        for thph in thps.find({}, {"_id": 0, "umbrella_filter_handler": 1, "value_handler": 1}):
            if thph.get("umbrella_filter_handler"):
                name = thph["umbrella_filter_handler"]
                if "umbrella_filter_handler" not in thp_handlers:
                    thp_handlers["umbrella_filter_handler"] = [thph["umbrella_filter_handler"]]
                elif name not in thp_handlers["umbrella_filter_handler"]:
                    thp_handlers["umbrella_filter_handler"].append(thph["umbrella_filter_handler"])
            if thph.get("value_handler"):
                name = thph["value_handler"]
                if "value_handler" not in thp_handlers:
                    thp_handlers["value_handler"] = [thph["value_handler"]]
                elif name not in thp_handlers["value_handler"]:
                    thp_handlers["value_handler"].append(thph["value_handler"])
        for h_type in thp_handlers:
            # Create handler
            for handler in thp_handlers[h_type]:
                h_id = bson.ObjectId()
                h_data = {
                    "_id": h_id,
                    "handler": handler,
                    "name": handler,
                    "description": "Migrated %s %s" % ("thresholdprofiles", handler),
                    HTYPE.get(h_type): True,
                }
                h_coll.insert_one(h_data)

    def migrate_change_handlers(self):
        h_coll = self.mongo_db["handlers"]
        thps = self.mongo_db["thresholdprofiles"]
        for thph in thps.find({}, {"_id": 1, "umbrella_filter_handler": 1, "value_handler": 1}):
            if thph.get("umbrella_filter_handler"):
                handler = h_coll.find_one({"handler": thph["umbrella_filter_handler"]}, {"_id": 1})
                thps.update_one(
                    {"_id": thph["_id"]}, {"$set": {"umbrella_filter_handler": handler["_id"]}}
                )
            if thph.get("value_handler"):
                handler = h_coll.find_one({"handler": thph["value_handler"]}, {"_id": 1})
                thps.update_one({"_id": thph["_id"]}, {"$set": {"value_handler": handler["_id"]}})
