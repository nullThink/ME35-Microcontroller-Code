# 2 min in on video on https://edu-content-preview.arduino.cc/content-preview/university/project/CONTENTPREVIEW+AEKR2

import time
from motorController import *

board = NanoMotorBoard()

print("reboot")
board.reboot()
time.sleep_ms(500)

motors = []

# at 50 it works as expected, at 60 shift sides and is too small duty to move, at 70 is very big duty.
for i in range(2):
    motors.append(DCMotor(i))

# Reset the encoder internal counter to zero (can be set to any initial value)
for motor in motors:  # initialize
    b = motor.setDuty(0)
    b = motor.resetEncoder(0)

heartEncoderValues = [
{
    "M1": 288, 
    "M2": 523
},{
  "M1":405,
  "M2":523
},{
  "M1":378,
  "M2":470
},{
  "M1":351,
  "M2":414
},{
  "M1":428,
  "M2":413
},{
  "M1":519,
  "M2":463
},{
  "M1":559,
  "M2":413
},{
  "M1":638,
  "M2":414
},{
  "M1":666,
  "M2":470
},{
  "M1":692,
  "M2":523
},{
  "M1":287,
  "M2":575
}]

def executeHeart():
    for position in heartEncoderValues:
        moveToEncoderPosition(motors[0], position["M1"])
        moveToEncoderPosition(motors[1], position["M2"])
        time.sleep(1)

def moveToEncoderPosition(motorToMove, desiredPosition):
    startingPosition = motorToMove.readEncoder()
    currentPosition = startingPosition
    
    if(startingPosition > desiredPosition):
        while(currentPosition > desiredPosition):
            motorToMove.setDuty(27)
            currentPosition = motorToMove.readEncoder()
            print(currentPosition)
    else:
        while(currentPosition < desiredPosition):
            motorToMove.setDuty(-27)
            currentPosition = motorToMove.readEncoder()
            print(currentPosition)

    motorToMove.setDuty(0)
    
executeHeart()

while True:
    for motor in motors:
        print("Encoder Pos [counts]: {0}".format(motor.readEncoder()))
        #print(" Encoder%d vel [counts/sec]: %d" % (i, motor.getCountPerSecond()))
    #Keep active the communication between Nano & Motor Carrier
    board.ping()
    time.sleep_ms(100)
