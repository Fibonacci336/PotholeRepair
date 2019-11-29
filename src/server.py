# import the necessary packages
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import vision
import distance
import json
import infrared


# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

vs = VideoStream(usePiCamera=1, resolution=(400, 300)).start()
time.sleep(2)

lastDetectedTemps = []

def applyComputerVision(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
    global vs, outputFrame, lock
    md = vision.vision()
    #Run Computer vision algorithms
    total = 0

    distances = []

    currentTick = 0

    while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        frame = imutils.rotate(frame, 180)
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # for i in range(0, len(distances)):
        #     currentDistance = distances[i]
        #     distanceText = "Sensor " + str(i+1) + ": " + '{0:.2f}'.format(currentDistance) + " cm"

        #     textY = (frame.shape[0]-(10*i)-(5+(5*i)))
        #     textX = 5

        #     cv2.putText(frame, distanceText, (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
 
		# grab the current timestamp and draw it on the frame
        # timestamp = datetime.datetime.now()
        # cv2.putText(frame, timestamp.strftime(
		# 	"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        with lock:
            outputFrame = frame.copy()


def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
 
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
 
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
 
			# ensure the frame was successfully encoded
			if not flag:
				continue
 
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/sensor_data")
def sensor_data():

	#Setup Distances
	distance.initAllSensors()
	sensorMap = {}
	distanceList = distance.getAllDistances()
	sensorMap["distances"] = distanceList

	#Setup temp
	global lastDetectedTemps
	tempsMap = {"ambient" : lastDetectedTemps[0], "object" : lastDetectedTemps[1]}
	sensorMap["temperatures"] = tempsMap
	
	return Response(json.dumps(sensorMap), mimetype="text/json")


def getNewTempData():
	global lastDetectedTemps
	while True:
		lastDetectedTemps = infrared.getTemperature()
		time.sleep(0.5)

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
 
	# start a thread that will perform motion detection
	t = threading.Thread(target=applyComputerVision, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()

	tempT = threading.Thread(target=getNewTempData)
	tempT.daemon = True
	tempT.start()
 
	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)

 
# release the video stream pointer
vs.stop()
