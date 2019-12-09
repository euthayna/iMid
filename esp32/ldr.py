from  machine import ADC, Pin
import time
import _thread

adc_ldr = ADC(Pin(32));

def get_ldr(thread_name, client):
 while True:
  ldr_value= str(adc_ldr.read())
  msg = '{ "metrics": {"sensor": "ldr", "value": %s}}'  % ldr_value
  client.publish_metric(msg)
  print(ldr_value)
  _thread.exit()
