import RPi.GPIO as GPIO
import time
import math
import requests, json
import urllib
import ssl
import paho.mqtt.client as mqtt
import Adafruit_DHT
#import lcdlib

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


sensor = Adafruit_DHT.DHT11
dht11_pin = 4
light_pin = 33

Broker = "a12lfykiku14pr-ats.iot.us-west-2.amazonaws.com"
port = 8883

temp=0.0
humidity = 0.0


GPIO.setup(light_pin,GPIO.IN)
client = mqtt.Client()
client.tls_set("root-CA.pem", 
            certfile="demo.pem.crt", 
            keyfile="demo-private.pem.key", 
            cert_reqs=ssl.CERT_REQUIRED, 
            tls_version=ssl.PROTOCOL_TLSv1_2, 
            ciphers=None)

client.connect(Broker,port)
 
topic = "home/light"

try:
    while True:
    
        #IR Snesor
        print("---------------------")
        print("start Reading sensor values....")
        time.sleep(2)
        #print()
        humidity, temp = Adafruit_DHT.read_retry(sensor, dht11_pin)
        light_status = GPIO.input(light_pin)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            #print("Temparature and Humidity sensor value")
            print()
            print("Temparature = %.02f C"%(temp))
            print("--------")
            print()
            print("Humidity = %.02f%%"%(humidity))
            print("--------")
        print("light status : "+str(light_status))   
        data = payload = json.dumps({"temp":temp,"Humidity":humidity,"light_status":light_status})
        client.publish(topic,data)
        print("")
        print("Published data to cloud")
        print("")
        print("")
        time.sleep(1)
##        
except TypeError:
       print ("type error")
except KeyboardInterrupt:
       print ("IO Error")
       GPIO.cleanup()
