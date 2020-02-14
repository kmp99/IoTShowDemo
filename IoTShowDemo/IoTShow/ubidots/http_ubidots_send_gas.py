from ubidots import ApiClient
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)                     #Set GPIO pin numbering 

buzzer_pin = 36                                  #Associate pin 23 to TRIG

GPIO.setup(buzzer_pin,GPIO.OUT)                                 #Associate pin 24 to ECHO
api = ApiClient(token='BBFF-YA8u8UuaZj33grdyau07Trbmz7GUXp')
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


try:
    variable1 = api.get_variable("5e145b171d84721ef08f3c83")
    

except ValueError:
    print("It is not possible to obtain the variable")

while(1):
    try:
          value1 = mcp.read_adc(0)
          print("Gas Value : ")
          print(value1)
          variable1.save_value({'value': value1})
          if(value1 > 400):
              print("Gas is leaking please be alert")
              GPIO.output(buzzer_pin,1)
          else:
              print("No Gas Leakage")
              GPIO.output(buzzer_pin,0)
          print("Value sent")
          time.sleep(1)
    except ValueError:
        GPIO.cleanup()
        print("Value not sent")
