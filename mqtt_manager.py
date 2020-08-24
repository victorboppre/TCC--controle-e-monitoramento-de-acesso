'''
Created on 20 de ago de 2018

@author: Victor
'''
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

Broker = "iot.eclipse.org"
PortBroker = 1883
KeepAliveBroker = 60
timeOut = 1000
#Callback - when a new msg is received
def on_message(client, userdata, msg):
    global a
    a = msg.payload

#Method to wait a msg:
def get_msg(topicSubscribe):
    times = 0
    client = mqtt.Client()
    client.on_message = on_message
    global a
    a = b''
    return a
    client.connect(Broker, PortBroker, KeepAliveBroker)
    client.subscribe(topicSubscribe)
    client.loop_start()
    while a == b'' and times != 10:
        time.sleep(1)
        times+=1
    return a
#Method to send a new message via MQTT
def set_msg(topicSubscribe,payload):
    publish.single(topicSubscribe, payload, hostname="iot.eclipse.org")