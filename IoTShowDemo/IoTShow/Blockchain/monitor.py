from ethjsonrpc import EthJsonRpc
import time
import sys,traceback
import datetime
import glob
import os
import Adafruit_DHT

##os.system('modprobe w1-gpio')
##os.system('modprobe w1-therm')
##
##base_dir = '/sys/bus/w1/devices/'
##device_folder = glob.glob(base_dir + '28*')[0]
##device_file = device_folder + '/w1_slave'
contract_address = '0x2c9472e0c6101f87d45c6301a8976a58447b5bba'
machineID1 = 1234
#machineID2 = 128
# Connect to Blockchain network
c = EthJsonRpc('192.168.43.212', 8545)
tempCount = 0
tempThreshold = 20 #Celcius
tempCountThreshold = 6
##def read_temp_raw():
##    f = open(device_file, 'r')
##    lines = f.readlines()
##    f.close()
##    return lines
## 
##def read_temp():
##    lines = read_temp_raw()
    
while True:
##    f = open(device_file, 'r')
##    lines = f.readlines()
##    
##    while lines[0].strip()[-3:] != 'YES':
##        time.sleep(0.2)
##        lines = read_temp_raw()
##    equals_pos = lines[1].find('t=')
##    if(equals_pos != -1):
##        temp_string = lines[1][equals_pos+2:]
##        temperature = float(temp_string)/1000.0
##        print "Temp:", temperature, "C"
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print("Temperature")
    print(temperature);
    if(temperature>tempThreshold):
        tempCount = tempCount + 1
        ts = int(time.time())
        print ("ts: ", ts)
    if(tempCount>tempCountThreshold):
        print("temp gt threshol")
        #c.call_with_transaction(c.eth_coinbase(), contract_address, 'requestService(uint256,uint256,string)', [ts, machineID1, "Temperature is crossed Treshold"])
        c.call_with_transaction(c.eth_coinbase(), contract_address, 'requestService(uint256,uint256,string)', [ts, machineID1, "Please update your Software"])
        print ("aftre transaction")
        tempCount = 0
    time.sleep(1)
