import json
import time
import paho.mqtt.client as mqtt
from django.utils import timezone

class DBconnectedMQTTClient(mqtt.Client):
    pass

def updateSubscriptions():
    from .models import registry
    from django.apps import apps
    appconfig = apps.get_app_config('archiver')
    while True:
        subscribedSigs = (str(sig.signal)
                for sig in registry.objects.all()
                if sig.archival_active)
        unsubscribedSigs = (str(sig.signal)
                for sig in registry.objects.all()
                if not sig.archival_active)
        for sig in subscribedSigs:
            appconfig.client.subscribe(sig)
        for sig in unsubscribedSigs:
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

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print "Connected!"
        else:
            print "Connection failed"

    def on_message(client, userdata, msg):
        from .models import registry
        registeredSigs = (sig.signal for sig in registry.objects.all()
                                if sig.archival_active)
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
                    timestamp = ts,
                    ).save()

    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(userName, userKey)
    client.connect(
            brokerAddress,
            brokerPort,
            brokertimeout)

    return client
