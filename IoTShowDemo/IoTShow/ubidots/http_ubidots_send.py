from ubidots import ApiClient
import random
import time
import sys
import Adafruit_DHT

#Set the type of sensor and the pin for sensor
sensor = Adafruit_DHT.DHT11
pin = 4

# Create an ApiClient object

api = ApiClient(token='BBFF-N7dybIQydlpl9RtYqAzuCP6pQoe7NE')

# Get a Ubidots Variable

try:
    variable1 = api.get_variable("5e43c0d81d847231eaea8844")
    variable2 = api.get_variable("5e43c0e01d84723245f65584")

except ValueError:
    print("It is not possible to obtain the variable")

while(1):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        print("Temp = "+str(temperature)+", Humidity = "+str(humidity))
        variable1.save_value({'value': temperature})
        variable2.save_value({'value': humidity})
        print("Value sent")
        time.sleep(120)
    except ValueError:
        print("Value not sent")
