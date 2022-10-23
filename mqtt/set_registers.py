import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import time
import json
import os

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
ROOM = os.environ.get('ROOM')
HOTWSTART = os.environ.get('HOTWSTART')
HOTWSTOP = os.environ.get('HOTWSTOP')
REDUCTION = os.environ.get('REDUCTION')

def file_is_older_than(file, delta):
    cutoff = datetime.utcnow() - delta
    mtime = datetime.utcfromtimestamp(os.path.getmtime(file))
    if mtime < cutoff:
        return True
    return False

def on_message(client, userdata, message):
    msg = str( message.payload.decode("utf-8"))
    print(f"RECEIVED {msg}")
    d  = json.loads(msg)
    vptime = d['d104']
    print(f"vptime = {vptime}")
    temp = d['d68']
    print(f"hw={temp}")
    room = d['d50']
    print(f"room={room}")
    hotwstart = d['d68']
    print(f"hotwstart={hotwstart}")
    hotwstop = d['d84']
    print(f"hotwstop={hotwstop}")
    hotw = d['d7']
    print(f"hotw = {hotw}")
    t = datetime.now()
    fn  = "/home/ostlund/WWW/thermiq-docker/pv/data.out"
    if file_is_older_than( fn, timedelta( seconds=70)):
        with open("/home/ostlund/WWW/thermiq-docker/pv/data.out","a" ) as f:
            print(f"{t} {d}", file=f)


def on_log(client, userdata, level, buf):
    print("log: ",buf)
    pass

client = mqtt.Client("P1")
topic = "ThermIQ/ThermIQ-mqtt-bb/data"
print(f" HOTWSTART = {HOTWSTART}")
client.on_message=on_message 
client.on_log = on_log
client.username_pw_set(username=USERNAME ,password=PASSWORD)
client.connect("10.0.0.182",port=9883,keepalive=60,bind_address="")
client.loop_start()

#s = '{"d59":' + REDUCTION + '}'
#print(f"json1 = {s}")
#client.publish("ThermIQ/ThermIQ-mqtt-bb/WRITE",s)
#res = client.publish("ThermIQ/ThermIQ-mqtt-bb/READ" )

s = '{"d50":' + ROOM + '}'
print(f"json1 = {s}")
client.publish("ThermIQ/ThermIQ-mqtt-bb/WRITE",s)

#client.wait_for_publish()
res = client.publish("ThermIQ/ThermIQ-mqtt-bb/READ" )
print(f"res = {res}")
#s3 = '{"d84":' + HOTWSTOP + '}'
#print(f"json3 = {s3}")
#client.publish("ThermIQ/ThermIQ-mqtt-bb/WRITE",s3)
#client.wait_for_publish()
#res3 = client.publish("ThermIQ/ThermIQ-mqtt-bb/READ" )
#print(f"res={res3}")

#s2 = '{"d68":' + HOTWSTART + '}'
#print(f"json2 = {s2}")
#client.publish("ThermIQ/ThermIQ-mqtt-bb/WRITE",s2)
#client.wait_for_publish()
res2 = client.publish("ThermIQ/ThermIQ-mqtt-bb/READ" )
#print(f"res={res2}")
client.subscribe(topic)
time.sleep(60)
client.loop_stop()
