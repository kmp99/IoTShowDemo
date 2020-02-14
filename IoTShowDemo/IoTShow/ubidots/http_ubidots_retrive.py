import time
from ubidots import ApiClient

api = ApiClient(token='BBFF-N7dybIQydlpl9RtYqAzuCP6pQoe7NE')

try:
    variable1 = api.get_variable("5e43c0d81d847231eaea8844")
    #variable2 = api.get_variable("5c2ef71ac03f976984838b7e")

except ValueError:
    print("It is not possible to obtain the variable")

while True:
    temp_str = variable1.get_values(1)
    #print(dist_str[0])
    temp_value = temp_str[0]['value']
    print(temp_value)
    if(temp_value<23):
        print('Normal Temperature')
    else:
        print('High Temperature')
    time.sleep(10)
