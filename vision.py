from picamera import PiCamera
from picamera.array import PiRGBArray

import cv2

class vision():
    def __init__(self):
        print("Vision!")

def takePicture():
    camera = PiCamera()
    camera.rotation = 180
    camera.capture("lastImage.jpg")
    return cv2.imread("lastImage.jpg", 0)
