# Credit to Chris Rogers for his code
# in Test-Servo.py under this GitHub repo
# https://github.com/chrisbuerginrogers/ME35_21/tree/main/SampleCodes/Motor%20Carrier

import time
from motorController import *

board = NanoMotorBoard()
print("reboot")
board.reboot()
time.sleep_ms(500)

servos = []

for i in range(1,3,1):
    servos.append(Servo(i))

#if (!PMIC.enableBoostMode()):
#    print("Error enabling Boost Mode");\

while True:
    for i in range(0,180,180):  # Servo sweep from 0 position to 90
        # Choose which of the servo connectors you want to use: servo1(default), servo2, servo3 or servo4
        for servo in servos:
            reply = servo.setAngle(i)
            time.sleep_ms(0)
        print("Servos position: %d" % i)
        
    time.sleep_ms(1000)
    for i in range(180,0,-180): # Servo sweep from 90 position to 0
        # Choose which of the servo connectors you want to use: servo1(default), servo2, servo3 or servo4
        for servo in servos:
            reply = servo.setAngle(i)
            time.sleep_ms(0)
        print("Servos position: %d" % i)
    # Keep active the communication between MKR board & MKR Motor Carrier
    # Ping the SAMD11
    board.ping()
    time.sleep_ms(1000)
