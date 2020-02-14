import time
from ubidots import ApiClient
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
buzzer_pin = 38


GPIO.setup(buzzer_pin, GPIO.OUT)

api = ApiClient(token='BBFF-N7dybIQydlpl9RtYqAzuCP6pQoe7NE')

try:
    variable1 = api.get_variable("5e43c0e81d847230e49d0b00")
    

except ValueError:
    print("It is not possible to obtain the variable")

while True:
    try:
        light_str = variable1.get_values(1)
        light_value = light_str[0]['value']
        #print(light_value)
        if(light_value == 1):
            print('Alert ! Room is Dark ')
            GPIO.output(buzzer_pin,1)
        else:
            #print('Alert ! Room is Dark ')
            GPIO.output(buzzer_pin,0)

        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
    
