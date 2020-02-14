import RPi.GPIO as gpio
import time
import math
import requests, json
import urllib
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

Broker = "162.255.85.191"
port = 1883

client = mqtt.Client()

client.connect(Broker,port)
topic = "device/5ca3cb9ff1327c04c1ec1338"

def glow_led(event):
    lcd.lcd_init()
    if event == switch1 :
        lcd.lcd_string("switch1 pressed",0x80)
        lcd.lcd_string("Street Light1 ON",0xc0)
        print "Object detected near Street light 1"
        print "Turning On Street Light1"
        data=json.dumps([{"sensor" : "sc-street-lights", "value":1, "timestamp":"", "context":"Street Lights"}])
        gpio.output(led1, True)
        time.sleep(2)
        gpio.output(led1, False)
    
    if event == switch2 :
        lcd.lcd_string("switch2 pressed",0x80)
        lcd.lcd_string("Street Light2 ON",0xc0)
        print "Object detected near Street light 2"
        print "Turning On Street Light2"
        data=json.dumps([{"sensor" : "sc-street-lights", "value":2, "timestamp":"", "context":"Street Lights"}])
        gpio.output(led2, True)
        time.sleep(2)
        gpio.output(led2, False)
        
    
    if event == switch3 :
        lcd.lcd_string("switch3 pressed",0x80)
        lcd.lcd_string("Street Light3 ON",0xc0)
        print "Object detected near Street light 3"
        print "Turning On Street Light3"
        data=json.dumps([{"sensor" : "sc-street-lights", "value":3, "timestamp":"", "context":"Street Lights"}])
        gpio.output(led3, True)
        time.sleep(2)
        gpio.output(led3, False)
    
    if event == switch4 :
        lcd.lcd_string("switch4 pressed",0x80)
        lcd.lcd_string("Street Light4 ON",0xc0)
        print "Object detected near Street light 4"
        print "Turning On Street Light4"
        data=json.dumps([{"sensor" : "sc-street-lights", "value":4, "timestamp":"", "context":"Street Lights"}])
        gpio.output(led4, True)
        time.sleep(2)
        gpio.output(led4, False)
    
    client.publish(topic,data)
    print("")
    print("Published data to cloud")
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
