import subprocess
import shlex
import RPi.GPIO as GPIO
from time import sleep

def celsiusToFahrenheit(cel):

    if(isinstance(cel, str)):
        cel = float(cel)

    return (9.0/5.0 * cel + 32)

#R
# eturns (Ambient Temperature, Object Temperature)
# def getTemperature(isCelsius=False):
#     command = subprocess.Popen(["sudo", "./tempProgram/temp"], stdout=subprocess.PIPE)
#     output = command.communicate()
#     command.wait()
#     output = output[0]
#     output = str(output,'utf-8')

#     temps = []
#     for temp in output.split(" "):
#         if(isCelsius):
#             temps.append(float(temp))
#             continue
#         temps.append(celsiusToFahrenheit(temp))
#     return temps

def switchHeaterState(setOn):
    GPIO.setmode(GPIO.BCM)

    gpioPin = 20

    GPIO.setup(gpioPin, GPIO.OUT)

    if(setOn):
        GPIO.output(gpioPin, GPIO.HIGH)
    else:
        GPIO.output(gpioPin, GPIO.LOW)


# while(True):
#     temperatures = getTemperature()
#     print("Ambient Temp: " + str(round(temperatures[0], 2)) + "ºF")
#     print("Object Temp: " + str(round(temperatures[1], 2)) + "ºF")
try:
    isOn = False
    while True:
        if not isOn:
            switchHeaterState(True)
            isOn = True
except:
    switchHeaterState(False)
