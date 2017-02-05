from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils import timezone
from threading import Thread
import paho.mqtt.client as mqtt
import json
import time

def startMQTT(cpm):
    with open('itsmqttbroker.dat', 'r') as brokerFile:
        jsonBrokerObj = json.load(brokerFile)
    brokerAddress = jsonBrokerObj['broker'].encode().replace('tcp://', '')
    brokerPort = jsonBrokerObj['brokerport'].encode()
    userName = jsonBrokerObj['key'].encode()
    userKey = jsonBrokerObj['secret'].encode()
    brokertimeout = 60

    client = mqtt.Client(
        client_id = "ExperimentalArchiver",
        clean_session = False,
        userdata = None)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.subscribe('itsGeiger01/get/#')
            print "Connected!"
        else:
            print "Connection failed"

    def on_message(client, userdata, msg):
        if 'itsGeiger01/get/cpm' in msg.topic:
            jsonPayload = json.loads(msg.payload)
            val = cpm(measured_val = int(jsonPayload['cpmGet']), timestamp = timezone.now())
            val.save()
            print len(cpm.objects.all())

    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(userName, userKey)
    client.connect(
            brokerAddress,
            brokerPort,
            brokertimeout)

    client.loop_start()

class ArchiverConfig(AppConfig):
    name = 'archiver'

    def ready(self):
        from .models import cpm
        startMQTT(cpm)
