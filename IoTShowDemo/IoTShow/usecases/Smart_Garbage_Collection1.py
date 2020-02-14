import RPi.GPIO as GPIO
import time
import math
import requests, json
import urllib2
import paho.mqtt.client as mqtt
import Adafruit_DHT
import lcdlib

GPIO.setmode(GPIO.BCM)

GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.IN)

trig_pin = 19
echo_pin = 26
Broker = "162.255.85.191"
port = 1883


distance = 0.0
duration = 0.0

myAPI = '67M4VWQI9AVB0BAG'
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
lcdlib.lcd_init()
try:
    while True:
    
        #IR Snesor
        print("---------------------")
        print("start Reading sensor values....")
        time.sleep(2)
        print("---------------------")
        
        GPIO.output(trig_pin, False)                 #Set TRIG as LOW
        print ('Waitng For Sensor To Settle')
        time.sleep(2)                            #Delay of 2 seconds

        GPIO.output(trig_pin, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(trig_pin, False)                 #Set TRIG as LOW

        while GPIO.input(echo_pin)==0:               #Check whether the ECHO is LOW
            pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(echo_pin)==1:               #Check whether the ECHO is HIGH
            pulse_end = time.time()                #Saves the last known time of HIGH pulse 

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)            #Round to two decimal points
        max = 200
        if distance > 2 and distance < 400:      #Check whether the distance is within range
            print ("Distance:",distance - 0.5,"cm")
            garbage_level = 100-(100*float(distance-0.5)/max)
            print ("{0:.0f}% full".format(garbage_level))
            if garbage_level > 65:
                print ("Sending text to Pick up garbage bin 1")
        else:
            print ("Out Of Range")
        
#       lcdlib.lcd_string("GEOFF",0x80)
        lcdlib.lcd_string("Garb Lvl:"+str(int(garbage_level))+"%",0x80)

        conn = urllib2.urlopen(baseURL + '&field4=%s' % int(garbage_level))
        print(" ")
        print("Published data to cloud")
        print(" ")
        print(" ")
        time.sleep(15)
     
except TypeError:
       print ("type error")
except KeyboardInterrupt:
       print ("IO Error")
       GPIO.cleanup()
