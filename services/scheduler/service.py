#!./bin/python
# ----------------------------------------------------------------------
# Scheduler
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.config import config
from noc.core.service.tornado import TornadoService
from noc.core.scheduler.scheduler import Scheduler


class SchedulerService(TornadoService):
    name = "scheduler"
    leader_lock_name = "scheduler"
    use_mongo = True

    async def on_activate(self):
        self.scheduler = Scheduler(
            "scheduler", reset_running=True, max_threads=config.scheduler.max_threads
        )
        self.scheduler.run()


if __name__ == "__main__":
    SchedulerService().start()
