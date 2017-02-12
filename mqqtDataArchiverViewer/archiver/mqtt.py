import json
import time
import paho.mqtt.client as mqtt
from django.utils import timezone

def subscribedSigsInDB():
    from .models import registry
    sigs = (
        str(sig.signal)
        for sig in registry.objects.filter(archival_active = True)
        )
    return sigs

def unsubscribedSigsInDB():
    from .models import registry
    sigs = (
        str(sig.signal)
        for sig in registry.objects.filter(archival_active = False)
        )
    return sigs

class DBconnectedMQTTClient(mqtt.Client):
    def __init__(self, *args, **kwargs):
        self.subscriptions = set()
        return super(DBconnectedMQTTClient, self).__init__(*args, **kwargs)

    def subscribe(self, topic):
        if not topic in self.subscriptions:
            self.subscriptions.add(topic)
            print self.subscriptions
            return super(DBconnectedMQTTClient, self).subscribe(topic)

    def unsubscribe(self, topic):
        if topic in self.subscriptions:
            self.subscriptions.remove(topic)
            print self.subscriptions
            return super(DBconnectedMQTTClient, self).unsubscribe(topic)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            from .models import registry
            print "Connected!"
            for sig in subscribedSigsInDB():
                client.subscribe(sig)
        else:
            print "Connection failed"

def updateSubscriptions():
    from .models import registry
    from django.apps import apps
    appconfig = apps.get_app_config('archiver')
    while True:
        for sig in subscribedSigsInDB():
            appconfig.client.subscribe(sig)
        for sig in unsubscribedSigsInDB():
            appconfig.client.unsubscribe(sig)
        time.sleep(1)

def startMQTT():
    with open('itsmqttbroker.dat', 'r') as brokerFile:
        jsonBrokerObj = json.load(brokerFile)
    brokerAddress = jsonBrokerObj['broker'].encode().replace('tcp://', '')
    brokerPort = jsonBrokerObj['brokerport'].encode()
    userName = jsonBrokerObj['key'].encode()
    userKey = jsonBrokerObj['secret'].encode()
    brokertimeout = 60

    client = DBconnectedMQTTClient(
        client_id = "ExperimentalArchiver",
        clean_session = False,
        userdata = None)

    def on_message(client, userdata, msg):
        from .models import registry
        registeredSigs = (
            str(sig.signal)
            for sig in registry.objects.filter(archival_active = True)
            )
        if not msg.topic in registeredSigs:
            return
        if 'itsPowerMeter01/get' in msg.topic:
            from .models import RFPowerMeter
            ts = timezone.now()
            jsonPayload = json.loads(msg.payload)
            RFPowerMeter(
                    input1 = float(jsonPayload['power1']),
                    input2 = float(jsonPayload['power2']),
                    timestamp = ts,
                    ).save()

        if 'itsSolarMeter01/get/cond' in msg.topic:
            from .models import TestStandEnvironment
            ts = timezone.now()
            jsonPayload = json.loads(msg.payload)
            TestStandEnvironment(
                    light = float(jsonPayload['photoGet']),
                    light_averaged = float(jsonPayload['photoAvgGet']),
                    temperature = float(jsonPayload['tempGet']),
                    timestamp = ts,
                    ).save()

        if 'itsGeiger01/get/cpm' in msg.topic:
            from .models import cpm
            ts = timezone.now()
            jsonPayload = json.loads(msg.payload)
            cpm(
                measured_val = int(jsonPayload['cpmGet']),
                timestamp = ts,
                ).save()

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
                    timestamp = ts,
                    ).save()

    client.on_message = on_message
    client.username_pw_set(userName, userKey)
    client.connect(
            brokerAddress,
            brokerPort,
            brokertimeout)

    return client
