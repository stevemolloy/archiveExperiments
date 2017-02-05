import json
import time
from threading import Thread
import paho.mqtt.client as mqtt
from django.utils import timezone

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
    from .models import cpm
    if 'itsGeiger01/get/cpm' in msg.topic:
        jsonPayload = json.loads(msg.payload)
        val = cpm(measured_val = int(jsonPayload['cpmGet']), timestamp = timezone.now())
        val.save()
        print cpm.objects.all()

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(userName, userKey)
client.connect(
        brokerAddress,
        brokerPort,
        brokertimeout)
