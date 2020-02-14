from ubidots import ApiClient
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)                     #Set GPIO pin numbering 

light_pin = 33
relay_pin = 36                                  #Associate pin 23 to TRIG
light_status = 0

GPIO.setup(light_pin,GPIO.IN)                                 #Associate pin 24 to ECHO
GPIO.setup(relay_pin,GPIO.OUT)                                 #Associate pin 24 to ECHO
api = ApiClient(token='BBFF-N7dybIQydlpl9RtYqAzuCP6pQoe7NE')

try:
    variable1 = api.get_variable("5e43c0e81d847230e49d0b00")
    

except ValueError:
    print("It is not possible to obtain the variable")

while(1):
    try:
          light_status = GPIO.input(light_pin)
          if(light_status == 0):
              print("Bright Outside Relay OFF")
              GPIO.output(relay_pin,0)
              variable1.save_value({'value': light_status})
          else:
              print("Dark Outside Relay ON")
              GPIO.output(relay_pin,1)
              variable1.save_value({'value': light_status})
              time.sleep(3)
          print("Value sent")
          time.sleep(1)
    except ValueError:
        GPIO.cleanup()
        print("Value not sent")
