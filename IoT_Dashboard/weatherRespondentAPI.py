import serial

s = serial.Serial('COM4', baudrate=115200)

import requests
from sensitive.py import APIKey as key

apiLink = 'http://api.weatherapi.com/v1/'
apiKey = key

city = input("What city and state do you want to know the temperature of? ")
    
r = requests.get(apiLink+"forecast.json?key="+apiKey+"&q="+city+"&days=1&aqi=no&alerts=no")
r.status_code

data = r.json()
temperature = data["current"]["temp_f"]

code1 = '''
from machine import Pin, Timer
import time

pins = ["D12", "D11", "D10", "D9", "D8", "D7", "D6", "D5", "D4", "D3"]

for pin in pins:
    Pin(pin, Pin.OUT).off()

for i in range(11):
    if({0} < i*10):
        break;
    else:
        Pin(pins[i], Pin.OUT).on() 
    time.sleep_ms(100)

'''.format(temperature)

CtrlC = '\x03'
CtrlD = '\x04'
CtrlE = '\x05'
s.write(CtrlE.encode())
code = code1.replace('\n','\r\n').encode()
print(code)
s.write(code)
s.write(CtrlD.encode())
print(s.read_all())

s.close()
