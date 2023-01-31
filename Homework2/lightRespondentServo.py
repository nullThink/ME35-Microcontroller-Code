from motorcontroller import *
from machine import Pin, ADC
import time
import math
 
board = NanoMotorBoard()
print("reboot")
board.reboot()
time.sleep_ms(500)
 
# Declare I/O pins for light sensor and potentiometer
lightInputPin = machine.Pin(28) #Pin A2
potInputPin = machine.Pin(29) #Pin A3

lightAin = machine.ADC(lightInputPin)
potAin = machine.ADC(potInputPin)

# Initialize servos and angle
servos = []

for i in range(4):
    servos.append(Servo(i))

servoAngleInit = math.floor((potAin.read_u16() / 68000) * 180)

for servo in servos:
    servo.setAngle(servoAngleInit)
    
# Question: Why do the servos only move when set up in a list? I try to call them individually but then it doesn't work at all

# operatingServo.setAngle(servoAngleInit)

# Gets the average ambient light of the room
# def getAmbientLight(sampleRate):
#     lightReadings = []
    
#     for i in range(10):
#         currentLight = lightAin.read_u16()
#         lightReadings.append(currentLight)
#         time.sleep_ms(sampleRate)
    
#     ambientAverage = sum(lightReadings)/len(lightReadings);
    
#     return ambientAverage

# baselineLight = getAmbientLight(100)
# print("\n Average Light: "+ str(baselineLight))

# Determines a general range for which the motor operates and rotates to
def initializeLightAngleRange():
    print("Cover the light sensor for 3 seconds.")
    darknessData = []
    brightnessData = []
    
    for i in range(30):
        darknessData.append(lightAin.read_u16())
        time.sleep_ms(100)
    
    print("Do not cover the light sensor for 3 seconds.")
    
    for i in range(30):
        brightnessData.append(lightAin.read_u16())
        time.sleep_ms(100)
    
    darkestValue = min(darknessData)
    brightestValue = max(brightnessData)
    
    #Points: (darkestValue, 0), (brightestValue, 180)
    slope = (180 - 0) / (brightestValue - darkestValue)
    
    # darkestValue ends up becoming the y-intercept of the equation
    return [slope, darkestValue, brightestValue]
    
def convertSignaltoAngle(signal):
    if(signal < lightToAngleConversionInformation[1]):
        return 0
    elif(signal > lightToAngleConversionInformation[2]):
        return 180
    else:
        return (lightToAngleConversionInformation[0]) * (signal - lightToAngleConversionInformation[1])

lightToAngleConversionInformation = initializeLightAngleRange()
print("Slope= "+ str(lightToAngleConversionInformation[0]) + "; Max Darkness= " + str(lightToAngleConversionInformation[1]))

while True:
    currentLightReading = lightAin.read_u16()
    angleToGo = math.floor(convertSignaltoAngle(currentLightReading))
    
    print("Light Value: " + str(currentLightReading) + "; Corresponding Angle: " + str(angleToGo))
    
    reply = servos[0].setAngle(angleToGo)
    
    time.sleep_ms(100)
