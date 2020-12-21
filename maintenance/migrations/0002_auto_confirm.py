# ----------------------------------------------------------------------
# Drop old maintenance
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime

# NOC modules
from noc.core.migration.base import BaseMigration
from noc.maintenance.models.maintenance import Maintenance


class Migration(BaseMigration):
    def migrate(self):
        now = datetime.datetime.now()
        changed = False
        for m in Maintenance.objects.filter(is_completed=False, auto_confirm__exists=False):
            if m.stop < now:
                changed = True
                m.is_completed = True
            elif m.stop > now:
                changed = True
                m.auto_confirm = True
            if changed:
                m.save()
                changed = False
