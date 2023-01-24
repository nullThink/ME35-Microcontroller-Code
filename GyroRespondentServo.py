import time
from lsm6dsox import LSM6DSOX
from motorController import *

from machine import Pin, I2C
lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))


board = NanoMotorBoard()
print("reboot")
board.reboot()
time.sleep_ms(500)

servos = []

for i in range(4):
    servos.append(Servo(i))    
    
while True():
    boardRotation = lsm.read_gyro()
    for servo in servos:
        servo.setAngle(boardRotation[0])
        time.sleep_ms(20)
    time.sleep_ms(200)
