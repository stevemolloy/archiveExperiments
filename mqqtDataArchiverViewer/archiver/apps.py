from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils import timezone
from threading import Thread
import paho.mqtt.client as mqtt
import json
import time

def startMQTT():
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
            client.subscribe('itsWaterSystem/get')
            print "Connected!"
        else:
            print "Connection failed"

    def on_message(client, userdata, msg):
        if 'itsGeiger01/get/cpm' in msg.topic:
            from .models import cpm
            ts = timezone.now()
            jsonPayload = json.loads(msg.payload)
            cpm(measured_val = int(jsonPayload['cpmGet']), timestamp = ts).save()

        if 'itsWaterSystem/get' in msg.topic:
            from .models import KlystronBodyWaterSystem
            from .models import ModOilTankWaterSystem
            from .models import KlystronCollectorWaterSystem
            from .models import KlystronSolenoidWaterSystem
            from .models import InputWaterSystem
            ts = timezone.now()
            jsonPayload = json.loads(msg.payload)
            KlystronBodyWaterSystem(
                    body_flow = float(jsonPayload['body']),
                    body_temp = None,
                    timestamp = ts,
                    ).save()
            ModOilTankWaterSystem(
                    tank_flow = float(jsonPayload['tank']),
                    tank_temp = None,
                    timestamp = ts,
                    ).save()
            KlystronCollectorWaterSystem(
                    collector_flow = float(jsonPayload['collector']),
                    collector_temp = None,
                    timestamp = ts,
                    ).save()
            KlystronSolenoidWaterSystem(
                    solenoid_flow = float(jsonPayload['solenoid']),
                    solenoid_temp = None,
                    timestamp = ts,
                    ).save()
            InputWaterSystem(
                    input_flow = None,
                    input_temp = float(jsonPayload['inputTemp']),
                    timestamp = ts,)
            val.save()

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
        startMQTT()
