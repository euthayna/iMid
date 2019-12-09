
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import ldr
import ujson
import temperature
import sys
import _thread
import gc

mqtt_server = "192.168.188.101"
mqtt_client = None

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("name", "password")

is_connected = False

def reload(mod):
    import sys
    mod_name = mod.__name__
    del sys.modules[mod_name]
    return __import__(mod_name)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

def debug_ota_after_pub():
  return "No debug"

class MyClient:
  connection = None
  topic_metrics = b'metrics'

  def __init__(self, host):
    self.host = host

  def connect(self):
    client_id = ubinascii.hexlify(machine.unique_id())

    if MyClient.connection is None:
      MyClient.connection = MQTTClient(client_id, self.host)
      MyClient.connection.set_callback(self.sub_callback)
      MyClient.connection.connect()
      print('Connected to %s MQTT broker' % (mqtt_server))

    return self.connection

  def check_msg(self):
    MyClient.connection.check_msg()

  # mqtt publish and subscript for metrics and versions
  def sub_callback(self, topic, msg):
    print(topic, msg)
    json = ujson.loads(msg)
    print(json)

    if topic == b'release_code':
      if json['code'] != None:
        try:
          exec(json['code'])
          file = open("ldr.py", "wb")
          file.write(json['code'])
          file.close()
          print("File ldr.py updated successfuly")

        except (SyntaxError, NameError) as e:
          print("Error executing new code. Will not update file.")


  def subscribe_to_topics(self):
    self.connect()
    MyClient.connection.subscribe(b'release_code')
    print('Subscribed to release_code topic')

  def publish_metric(self, msg):
    self.publish(MyClient.topic_metrics, msg)

  def publish(self, topic, msg):
    self.connect()
    MyClient.connection.publish(topic, msg)
    print('Published to %s: %s (%s)' % (topic, msg, debug_ota_after_pub()))

def restart_and_reconnect():
  print('Resetting machine...')
  machine.reset()

try:
  mqtt_client = MyClient(mqtt_server)
  mqtt_client.subscribe_to_topics()

except OSError as e:
  restart_and_reconnect()

i = 0
while True:
  try:
    mqtt_client.check_msg()
    time.sleep(1)
    gc.collect()

    reload(temperature)
    reload(ldr)
    import temperature
    import ldr


    _thread.start_new_thread(temperature.get_temp, ("Thread 1", mqtt_client, ))
    _thread.start_new_thread(ldr.get_ldr, ("Thread 2", mqtt_client, ))

    time.sleep(15)
    i += 1
  except OSError as e:
    restart_and_reconnect()
