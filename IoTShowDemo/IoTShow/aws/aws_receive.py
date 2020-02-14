import time
import os
#import motor_runner
import json
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
relay = 38
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay,GPIO.OUT)
GPIO.setwarnings(False) 
def callback_function(self, params, packet):
    print(packet.payload)
    msg = json.loads(packet.payload)
    temp_value = int(msg["temp"])
    if(temp_value > 28):
        print("Fan is ON")
        GPIO.output(relay,1)
    else:
        print("Fan is OFF")
        GPIO.output(relay,0)
myMQTTClient = AWSIoTMQTTClient("raspberryPiHome") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a12lfykiku14pr-ats.iot.us-west-2.amazonaws.com", 8883)
certRootPath = '/home/pi/AWS/certs/'
myMQTTClient.configureCredentials("{}root-CA.pem".format(certRootPath), "{}demo-private.pem.key".format(certRootPath), "{}demo.pem.crt".format(certRootPath))
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
 
myMQTTClient.connect()
myMQTTClient.subscribe("home/light", 1, callback_function)
 
def looper():
    while True:
        time.sleep(1) #sleep for 1 second and then sleep again
looper()
def function_handler(event, context):
    return
