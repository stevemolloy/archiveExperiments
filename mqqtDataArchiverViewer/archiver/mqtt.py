import json
import time
from threading import Thread
import paho.mqtt.client as mqtt

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
    print msg.topic, msg.payload

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(userName, userKey)
client.connect(
        brokerAddress,
        brokerPort,
        brokertimeout)
