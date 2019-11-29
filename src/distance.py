#Libraries
import RPi.GPIO as GPIO
import time
from enum import Enum

#Raw value: (Num, Trigger, Echo)
class DistanceSensors(Enum):
    SENSOR_1 = (1, 18, 25)
    SENSOR_2 = (2, 27, 5)
    SENSOR_3 = (3, 22, 6)
    SENSOR_4 = (4, 23, 12)
    SENSOR_5 = (5, 24, 13)

#Units (CM)
sensor_max_distance = 400
sensor_min_distance = 2

sensor_horizonal_distance = 200
sensor_vertical_distance = 100

 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

 
def initDistanceSensor(sensor):
    #set GPIO direction (IN / OUT)
    GPIO.setup(sensor.value[1], GPIO.OUT)
    GPIO.setup(sensor.value[2], GPIO.IN)

#Sensor enum value
def getDistance(sensor):

    #set GPIO Pins
    GPIO_TRIGGER = sensor.value[1]
    GPIO_ECHO = sensor.value[2]

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    # if(distance > sensor_max_distance or distance < sensor_min_distance):
    #     return -1
 
    return distance

def printDistance(sensor, distance):
    print("Sensor " + str(sensor.value[0]) + ": " + '{0:.2f}'.format(distance) + " cm")

def getAverageDistance():
    
    distances = getAllDistances()

    return (sum(distances)/len(distances))

def getAllDistances():
    distance1 = getDistance(DistanceSensors.SENSOR_1)
    distance2 = getDistance(DistanceSensors.SENSOR_2)
    distance3 = getDistance(DistanceSensors.SENSOR_3)
    distance4 = getDistance(DistanceSensors.SENSOR_4)
    distance5 = getDistance(DistanceSensors.SENSOR_5)

    return [distance1, distance2, distance3, distance4, distance5]


def initAllSensors():
    initDistanceSensor(DistanceSensors.SENSOR_1)
    initDistanceSensor(DistanceSensors.SENSOR_2)
    initDistanceSensor(DistanceSensors.SENSOR_3)
    initDistanceSensor(DistanceSensors.SENSOR_4)
    initDistanceSensor(DistanceSensors.SENSOR_5)

#def calculateVolume(sensorHeight):
