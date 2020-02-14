# Example of using the MQTT client class to subscribe to a feed and print out
# any changes made to the feed.  Edit the variables below to configure the key,
# username, and feed to subscribe to for changes.

# Import standard python modules.
import sys
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import Adafruit_DHT as DHT
import time

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW) # Set pin 38 to be an output pin and set initial value to low (off)
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW) # Set pin 36 to be an output pin and set initial value to low (off)
sensor_type = DHT.DHT11
sensor_pin = 4
#moisture = 19
# Set all pins as output
StepPins = [33,7,31,29]


#moisture = 19
# Set all pins as output
for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
            
StepCount = len(Seq)
StepDir = 2 # Set to 1 or 2 for clockwise

# Read wait time from command line
WaitTime = 10/float(1000)


# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = "b47bfa0f5cf0416abfc189880a3e18fe" 
ADAFRUIT_IO_USERNAME = "allambharath123"  # See https://accounts.adafruit.com
                                                    # to find your username.

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'buzzer'
FEED_ID1 = 'motor'
FEED_ID2 = 'bulb'
FEED_ID3 = 'temperature'
FEED_ID4 = 'humidity'
FEED_ID5 = 'temp_alert'



def run_motor_forward():
    # Set to -1 or -2 for anti-clockwise
     
    
    StepCounter = 0 
    # Start main loop
    for i in range(0,500):
      print StepCounter,
      print Seq[StepCounter]
     
      for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
          print " Enable GPIO %i" %(xpin)
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
     
      StepCounter += StepDir
     
      # If we reach the end of the sequence
      # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
        StepCounter = StepCount+StepDir
     
      # Wait before moving on
      time.sleep(0.01)
def run_motor_reverse():
    StepCounter = 0
     
    # Start main loop
    for i in range(0,500):
      print StepCounter,
      print Seq[StepCounter]
     
      for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
          print " Enable GPIO %i" %(xpin)
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
     
      StepCounter -= StepDir
     
      # If we reach the end of the sequence
      # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
        StepCounter = StepCount-StepDir
     
      # Wait before moving on
      time.sleep(0.01)

#run_motor_forward()
# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID)
    client.subscribe(FEED_ID1)
    client.subscribe(FEED_ID2)
    client.subscribe(FEED_ID5)
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
	if(feed_id == 'buzzer'):
		print('Feed {0} received new value: {1}'.format(feed_id, payload))
		if payload=='ON':
			GPIO.output(38, GPIO.HIGH)
			client.publish(FEED_ID,xtrans) # Turn on
		elif payload=='OFF':
			 GPIO.output(38, GPIO.LOW) # Turn off
	if(feed_id == 'motor'):
		print('Feed {0} received new value: {1}'.format(feed_id, payload))
		if payload=='OPEN':
			run_motor_forward()
		elif payload=='CLOSE':
			run_motor_reverse() 
	if(feed_id == 'bulb'):
		print('Feed {0} received new value: {1}'.format(feed_id, payload))
		if payload=='ON':
			GPIO.output(36, GPIO.HIGH)
		elif payload=='OFF':
			GPIO.output(36, GPIO.LOW) # Turn off
	if(feed_id == 'temp_alert'):
		print('Feed {0} updated with new value: {1}'.format(feed_id, payload))
		if payload=='ON':
			Humidity, Temperature = DHT.read_retry(sensor_type,sensor_pin)
			client.publish(FEED_ID3,Temperature)
		elif payload=='OFF':
			Humidity, Temperature = DHT.read_retry(sensor_type,sensor_pin)
			client.publish(FEED_ID4,Humidity)


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client.loop_blocking()




