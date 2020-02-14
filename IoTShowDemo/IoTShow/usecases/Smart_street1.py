import RPi.GPIO as GPIO
import time
import math
import requests, json
import urllib2
import paho.mqtt.client as mqtt
import Adafruit_DHT
#import lcdlib

trig_pin = 19
echo_pin = 26
led1 = 22
led2 = 18
led3 = 2
led4 = 3
light_pin = 13

GPIO.setmode(GPIO.BCM)

GPIO.setup(trig_pin,GPIO.OUT)
GPIO.setup(echo_pin,GPIO.IN)
GPIO.setup(light_pin,GPIO.IN)
GPIO.setup(led1,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(led2,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(led3,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(led4,GPIO.OUT,initial = GPIO.LOW)
Broker = "162.255.85.191"
port = 1883
count = 0

distance = 0.0
duration = 0.0
light_status = 0

myAPI = 'T51ATQNHSBCH9WHQ'
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
#lcdlib.lcd_init()
try:
    while True:
        count1=0
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
        distance = round(distance, 2)
        light_status = GPIO.input(light_pin)#Round to two decimal points
        print(light_status)
        print(distance)
        
        if distance < 20 and light_status == 1:      #Check whether the distance is within range
            print ("Street Light On for 5 Seconds")
            GPIO.output(led1,True)
            time.sleep(5)
            GPIO.output(led1,False)
            #time.sleep(5)
            count1+=1
            count+=1
            print(count)
            if(count1 == 10):
                #count+=10
                conn = urllib2.urlopen(baseURL + '&field4=%s' % int(count))
                print(" ")
                print("Published data to cloud")
                print(" ")
                print(" ")
                count1 = 0
        else:
            print ("Street Light is OFF")
            GPIO.output(led1,0)
        
#       lcdlib.lcd_string("GEOFF",0x80)
        #lcdlib.lcd_string("Count up to now:"+str(int(count))+"%",0x80)

        time.sleep(3)
     
except TypeError:
       print ("type error")
except KeyboardInterrupt:
       print ("IO Error")
       GPIO.cleanup()

