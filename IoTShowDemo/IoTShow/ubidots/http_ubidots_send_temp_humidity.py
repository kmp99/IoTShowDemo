from ubidots import ApiClient
import random
import time
import sys
import Adafruit_DHT

#Set the type of sensor and the pin for sensor
sensor = Adafruit_DHT.DHT11
pin = 4

# Create an ApiClient object

api = ApiClient(token='BBFF-YA8u8UuaZj33grdyau07Trbmz7GUXp')

# Get a Ubidots Variable

try:
    variable1 = api.get_variable("5e131ea01d847217cc345416")
    variable2 = api.get_variable("5e131e971d847216f02bce11")

except ValueError:
    print("It is not possible to obtain the variable")

while(1):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        print("Temp = "+str(temperature)+", Humidity = "+str(humidity))
        variable1.save_value({'value': humidity})
        variable2.save_value({'value': temperature})
        print("Value sent")
        time.sleep(1)
    except ValueError:
        print("Value not sent")
