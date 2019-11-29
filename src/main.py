import motor_control
from distance import *
from time import sleep
import RPi.GPIO as GPIO
import vision

DISPENSING_MOTOR = 4
REAR_DRIVE_MOTOR = 3

calibratedDepth = 0
depthMarginOfError = 1.5

def calibrate():
    initDistanceSensor(DistanceSensors.SENSOR_1)
    initDistanceSensor(DistanceSensors.SENSOR_2)
    initDistanceSensor(DistanceSensors.SENSOR_3)
    initDistanceSensor(DistanceSensors.SENSOR_4)
    initDistanceSensor(DistanceSensors.SENSOR_5)

    calibratedDepth = getAverageDistance()
    printDistance(DistanceSensors.SENSOR_1, calibratedDepth)

try:

    calibrate()
    motor_control.rotateDCMotor(REAR_DRIVE_MOTOR, 0.5)
    while True:

        if getAverageDistance() > calibratedDepth+depthMarginOfError:
            motor_control.stopDCMotor(REAR_DRIVE_MOTOR)
            



except KeyboardInterrupt:
    GPIO.cleanup()
