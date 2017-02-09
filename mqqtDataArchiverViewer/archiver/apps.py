from __future__ import unicode_literals

from django.apps import AppConfig
from .mqtt import startMQTT

class ArchiverConfig(AppConfig):
    name = 'archiver'

    def ready(self):
        from .models import registry
        client = startMQTT()
        client.loop_start()

        self.subscribedSigs = (sig.signal for sig in registry.objects.all() if sig.archival_active)
        for sig in self.subscribedSigs:
            client.subscribe(sig)

        self.client = client
