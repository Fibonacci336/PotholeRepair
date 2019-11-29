from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from time import sleep

def rotateStepper(steps, stepDirection=stepper.FORWARD):
    kit = MotorKit()
    for i in range(steps):
        kit.stepper1.onestep(direction=stepDirection, style=stepper.DOUBLE)
    
def rotateDCMotor(motorNum, throttlePower):
    kit = MotorKit()
    if(motorNum == 3):
        kit.motor3.throttle = throttlePower
    if(motorNum == 4):
        kit.motor4.throttle = throttlePower
    
def stopDCMotor(motorNum):
    rotateDCMotor(motorNum, 0)
