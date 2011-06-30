# -*- coding:utf-8 -*-
"""Dstat plugin, shows gearmand queues status.

Configuration via environment vars:

    GEARMAN_HOST (default: localhost)
    GEARMAN_PORT (default: 4730)
"""

global telnetlib
import telnetlib


class dstat_plugin(dstat):
    """Dstat plugin, shows gearmand queues status.
    """

    def __init__(self):
        self.nick = ('total', 'running', 'workers')
        self.type = 'd'
        self.width = 7
        self.scale = 0

        # Seconds telnetclient expects for an answer.
        self.timeout = 0.2
        self.client = self.gearman_connect()


    def gearman_connect(self):
        """Connect to Gearman.
        """
        host = os.getenv('GEARMAN_HOST') or 'localhost'
        port = os.getenv('GEARMAN_PORT') or '4730'
        
        return telnetlib.Telnet(host, port)



    def gearman_status(self):
        """Retrieve the 'status' of Gearman.
        """
        self.client.write('status\n')
        raw_status = self.client.expect(['^.$'], self.timeout)[2]
        # Format:
        # {queue_name: [total_jobs, running_jobs, available_workers], ... }
        lines = [ l for l in raw_status.split('\n') if l not in ['', '.'] ]
        fields = [ (l.split()[0], map(int, l.split()[1:])) for l in lines ]
        return dict(fields)


    def name(self):
        return self.gearman_status().keys()

    def vars(self):
        return self.name()
        
    def extract(self):
        self.val = self.gearman_status()

