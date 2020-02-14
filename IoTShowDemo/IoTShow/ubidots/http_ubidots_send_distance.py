from ubidots import ApiClient
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)                     #Set GPIO pin numbering 

TRIG = 35                                  #Associate pin 23 to TRIG
ECHO = 37
buzzer_pin = 38                                 #Associate pin 24 to ECHO

print("Distance measurement in progress")

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(buzzer_pin,GPIO.OUT)                  #Set pin as GPIO out
api = ApiClient(token='BBFF-N7dybIQydlpl9RtYqAzuCP6pQoe7NE')

try:
    variable1 = api.get_variable("5e43c0f31d8472331bd52336")
    

except ValueError:
    print("It is not possible to obtain the variable")

while(1):
    try:
          GPIO.output(TRIG, False)                 #Set TRIG as LOW
          print("Waitng For Sensor To Settle")
          time.sleep(2)                            #Delay of 2 seconds

          GPIO.output(TRIG, True)                  #Set TRIG as HIGH
          time.sleep(0.00001)                      #Delay of 0.00001 seconds
          GPIO.output(TRIG, False)                 #Set TRIG as LOW

          while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
            pulse_start = time.time()              #Saves the last known time of LOW pulse

          while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
            pulse_end = time.time()                #Saves the last known time of HIGH pulse 

          pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

          distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
          distance = round(distance)            #Round to two decimal points

          if distance > 2 and distance < 400:      #Check whether the distance is within range
            print("Distance:",distance,"cm")
          else:
            print("Out Of Range")                   #display out of range)

          variable1.save_value({'value': distance})
          print("Value sent")
          if(distance < 10):
            print("Distance less than 10 cm")
            GPIO.output(buzzer_pin,1)
          else:
            print("Distance Greater than 10 cm")
            GPIO.output(buzzer_pin,0)
          time.sleep(2)
    except ValueError:
        GPIO.cleanup()
        print("Value not sent")
