# ---------------------------------------------------------------------
# Update address database
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import os
import inspect
from configparser import SafeConfigParser

# NOC modules
from noc.core.management.base import BaseCommand, CommandError
from noc.gis.parsers.address.base import AddressParser
from noc.core.debug import error_report
from noc.config import config as cf
from noc.core.mongo.connection import connect


class Command(BaseCommand):
    help = "Update address database"

    def add_arguments(self, parser):
        parser.add_argument("--no-download", dest="download", action="store_false"),
        parser.add_argument("--download", dest="download", action="store_true", default=True),
        parser.add_argument(
            "--no-reset-cache", dest="reset_cache", action="store_false", default=False
        ),
        parser.add_argument("--reset-cache", dest="reset_cache", action="store_true", default=True)

    @staticmethod
    def get_parsers():
        parsers = []
        root = cf.gis.root_address
        for m in os.listdir(root):
            if m in ("__init__.py", "base.py"):
                continue
            p = os.path.join(root, m)
            if os.path.isfile(p) and p.endswith(".py"):
                parsers += [m[:-3]]
            elif os.path.isdir(p) and os.path.isfile(os.path.join(p, "__init__.py")):
                parsers += [m]
        return parsers

    def handle(self, *args, **options):
        #
        connect()
        parsers = []
        # Read config
        config = SafeConfigParser()
        sections = {
            "fias": {
                "enabled": cf.gis.enable_fias,
                "download_url": cf.gis.fias_download_url,
                "cache": cf.gis.fias_cache,
            },
            "oktmo": {"download_url": cf.gis.oktmo_download_url},
        }
        config._sections = sections
        for p in self.get_parsers():
            if cf.gis.enable_fias:
                m = __import__("noc.gis.parsers.address.%s" % p, {}, {}, "*")
                for i in dir(m):
                    a = getattr(m, i)
                    if inspect.isclass(a) and issubclass(a, AddressParser) and a != AddressParser:
                        parsers += [a]
            else:
                print("Parser '%s' is not enabled. Skipping.." % p)
        # Initialize parsers
        parsers = [p(config, options) for p in parsers]
        # Download
        if options["download"]:
            for p in parsers:
                # breakpoint()
                print("Downloading", p.name)
                if not p.download():
                    raise CommandError("Failed to download %s" % p.name)
        else:
            print("Skipping downloads")
        # Sync
        try:
            for p in parsers:
                print("Syncing", p.name)
                p.sync()
        except Exception:
            error_report()


if __name__ == "__main__":
    Command().run()
