from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils import timezone
from django.db.models.signals import post_save
from threading import Thread
import paho.mqtt.client as mqtt
import json
import time
import archiver
from .mqtt import startMQTT

class ArchiverConfig(AppConfig):
    name = 'archiver'

    def ready(self):
        client = startMQTT()

        client.loop_start()
