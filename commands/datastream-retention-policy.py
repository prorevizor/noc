# ---------------------------------------------------------------------
# ./noc datastream-retention-policy
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import datetime
import re

from bson.objectid import ObjectId

# NOC modules
from noc.core.management.base import BaseCommand
from noc.config import config
from noc.core.datastream.loader import loader
from noc.core.mongo.connection import connect


class Command(BaseCommand):
    help = "datastream-retention-policy"

    def add_arguments(self, parser):
        parser.add_argument("collection", action="store", type=str, help="Name collection")

    def handle(self, *args, **options):
        connect()
        collection_prefix = "ds_"

        start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            days=config.datastream.alarm_ttl
        )
        if not re.match(collection_prefix, options["collection"]):
            print("`Name collection` must be name of DataString collections.")
            return 0
        ds = loader[options["collection"].replace(collection_prefix, "")]
        collection = ds.get_collection()
        collection.delete_many({"_id": {"$lte": ObjectId.from_datetime(start_date)}})
        print(f"Records of {options['collection']} collection were deleted.")


if __name__ == "__main__":
    Command().run()
