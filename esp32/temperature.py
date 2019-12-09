import  machine
import onewire, ds18x20
import _thread

def get_temp(thread_name, client):
  ds_pin = machine.Pin(33)
  ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
  ds_sensor.convert_temp()

  for rom in ds_sensor.scan():
    temp = ds_sensor.read_temp(rom)
    msg = '{ "metrics": {"sensor": "temperature", "value": %s}}'  % temp
    client.publish_metric(msg)
  print('from temp: from form')
  _thread.exit()
