from __future__ import unicode_literals

from django.apps import AppConfig

import time
from threading import Thread

def linePrinting():
    x = 0
    while x<10:
        x += 1
        print("x = {}".format(x))
        time.sleep(1)


class ArchiverConfig(AppConfig):
    name = 'archiver'

    started = False

    def ready(self):
        if not self.started:
            self.started = True
            thread = Thread(target = linePrinting)
            thread.daemon = True
            thread.start()
