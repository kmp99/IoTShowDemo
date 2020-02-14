import RPi.GPIO as gpio
import time
import math
import requests, json
import urllib2
import paho.mqtt.client as mqtt
import lcdlib1 as lcd

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD) 
lcd.lcd_init()
led4 = 5    # pin is connected to LED and it should be OUT
led3 = 3     # pin is connected to LED and it should be OUT
led2 = 12     # pin is connected to LED and it should be OUT
led1 = 15   # pin is connected to LED and it should be OUT
switch4 = 23  # pin is connected to SWITC and it should be IN
switch3 = 21  # pin is connected to SWITC and it should be IN
switch2 = 19  # pin is connected to SWITC and it should be IN
switch1= 24 # pin is connected to SWITC and it should be IN

gpio.setup(led1,gpio.OUT,initial=0)
gpio.setup(led2,gpio.OUT,initial=0)
gpio.setup(led3,gpio.OUT,initial=0)
gpio.setup(led4,gpio.OUT,initial=0)
gpio.setup(switch1,gpio.IN)
gpio.setup(switch2,gpio.IN)
gpio.setup(switch3,gpio.IN)
gpio.setup(switch4,gpio.IN)

myAPI = 'YFHYN2DZ4VCRSSJ7'
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI

def glow_led(event):
    lcd.lcd_init()
    if event == switch1 :
        lcd.lcd_string("switch1 pressed",0x80)
        lcd.lcd_string("Street Light1 ON",0xc0)
        print "Object detected near Street light 1"
        print "Turning On Street Light1"
        value1 = 1
        gpio.output(led1, True)
        time.sleep(2)
        gpio.output(led1, False)
    else:
        value1 = 0
    
    if event == switch2 :
        lcd.lcd_string("switch2 pressed",0x80)
        lcd.lcd_string("Street Light2 ON",0xc0)
        print "Object detected near Street light 2"
        print "Turning On Street Light2"
        value2 = 1
        gpio.output(led2, True)
        time.sleep(2)
        gpio.output(led2, False)
    else:
        value2 = 0
        
    
    if event == switch3 :
        lcd.lcd_string("switch3 pressed",0x80)
        lcd.lcd_string("Street Light3 ON",0xc0)
        print "Object detected near Street light 3"
        print "Turning On Street Light3"
        value3 = 1
        gpio.output(led3, True)
        time.sleep(2)
        gpio.output(led3, False)
    else:
        value3 = 0
    
    if event == switch4 :
        lcd.lcd_string("switch4 pressed",0x80)
        lcd.lcd_string("Street Light4 ON",0xc0)
        print "Object detected near Street light 4"
        print "Turning On Street Light4"
        value4 = 1
        gpio.output(led4, True)
        time.sleep(2)
        gpio.output(led4, False)
    else:
        value4 = 0

    conn = urllib2.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s' % (value1,value2,value3,value4)) 
    print("Published data to cloud")
#    value1 = value2 = value3 = value4 = 0
    print("")
    print("")
gpio.add_event_detect(switch1, gpio.RISING , callback = glow_led, bouncetime = 100)
gpio.add_event_detect(switch2, gpio.RISING , callback = glow_led, bouncetime = 100)
gpio.add_event_detect(switch3, gpio.RISING , callback = glow_led, bouncetime = 100)
gpio.add_event_detect(switch4, gpio.RISING , callback = glow_led, bouncetime = 100)

try:
    while(True):
    #to avoid 100% CPU usage
        time.sleep(1)
except KeyboardInterrupt:
    #cleanup GPIO settings before exiting
    gpio.cleanup()
