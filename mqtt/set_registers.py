#!/home/ostlund/WWW/thermiq-docker/mqtt/env/bin/python
import paho.mqtt.client as mqtt
import time
import json

def on_message(client, userdata, message):
    msg = str( message.payload.decode("utf-8"))
    #print(f"RECEIVED {msg}")
    d  = json.loads(msg)
    vptime = d['d104']
    print(f"vptime = {vptime}")
    temp = d['d68']
    print(f"hw={temp}")


def on_log(client, userdata, level, buf):
    print("log: ",buf)
    pass

client = mqtt.Client("P1")
topic = "ThermIQ/ThermIQ-mqtt-bb/data"
client.on_message=on_message 
client.on_log = on_log
client.username_pw_set(username="thermiq",password="lissner")
client.connect("localhost",port=9883,keepalive=60,bind_address="")
client.loop_start()
client.publish("ThermIQ/ThermIQ-mqtt-bb/WRITE",'{"d68":39}')
res = client.publish("ThermIQ/ThermIQ-mqtt-bb/READ" )
print(f"res={res}")
client.subscribe(topic)
time.sleep(60)
client.loop_stop()
