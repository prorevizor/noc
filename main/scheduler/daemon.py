# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Legacy periodic scheduler
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
## Python modules
from __future__ import with_statement
import logging
## NOC modules
from noc.lib.daemon import Daemon
from periodic import PeriodicScheduler
from scheduler import JobScheduler
from noc.lib.stomp.threadclient import ThreadedSTOMPClient


class SchedulerDaemon(Daemon):
    daemon_name = "noc-scheduler"

    def __init__(self):
        self.stomp_host = None
        self.stomp_port = None
        self.stomp_client_id = None
        super(SchedulerDaemon, self).__init__()
        logging.info("Running noc-scheduler")
        self.periodic_thread = None
        self.scheduler = None
        self.stomp_client = None

    def load_config(self):
        super(SchedulerDaemon, self).load_config()
        self.stomp_host = self.config.get("stomp", "host")
        self.stomp_port = self.config.getint("stomp", "port")
        self.stomp_client_id = self.config.get("stomp", "client_id")

    def run(self):
        self.stomp_client = ThreadedSTOMPClient(
            self.stomp_host, self.stomp_port,
            client_id=self.stomp_client_id)
        self.stomp_client.start()
        self.scheduler = JobScheduler(self)
        self.periodic_thread = PeriodicScheduler(self)
        self.periodic_thread.start()
        self.scheduler.run()

    def send(self, message, destination,
             receipt=False, persistent=False, expires=None):
        self.stomp_client.send(message, destination,
            receipt=receipt, persistent=persistent, expires=expires)
