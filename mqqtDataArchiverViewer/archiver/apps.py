from __future__ import unicode_literals

from django.apps import AppConfig
from .mqtt import startMQTT

class ArchiverConfig(AppConfig):
    name = 'archiver'

    def ready(self):
        client = startMQTT()

        client.loop_start()
