import motor_control
from distance import *
from time import sleep
import RPi.GPIO as GPIO
import vision

try:
    #motor_control.rotateDCMotor(4,1)
    # motor_control.rotateStepper(5000)

    #sleep(10)
    #motor_control.stopDCMotor(4)

    # vision.takePicture()

    initDistanceSensor(DistanceSensors.SENSOR_1)
    initDistanceSensor(DistanceSensors.SENSOR_2)
    initDistanceSensor(DistanceSensors.SENSOR_3)
    initDistanceSensor(DistanceSensors.SENSOR_4)
    initDistanceSensor(DistanceSensors.SENSOR_5)

    while True:
        distance1 = getDistance(DistanceSensors.SENSOR_1)
        distance2 = getDistance(DistanceSensors.SENSOR_2)
        distance3 = getDistance(DistanceSensors.SENSOR_3)
        distance4 = getDistance(DistanceSensors.SENSOR_4)
        distance5 = getDistance(DistanceSensors.SENSOR_5)
        
        printDistance(DistanceSensors.SENSOR_1, distance1)
        printDistance(DistanceSensors.SENSOR_2, distance2)
        printDistance(DistanceSensors.SENSOR_3, distance3)
        printDistance(DistanceSensors.SENSOR_4, distance4)
        printDistance(DistanceSensors.SENSOR_5, distance5)
        print("------------------------------------------")
        sleep(0.1)

except KeyboardInterrupt:
        GPIO.cleanup()


