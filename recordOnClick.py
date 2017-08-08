# import the necessary packages
from __future__ import print_function
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
from camera_threaded import MyPiVideoStream
import argparse
import imutils
import time
import cv2

display = 0
safeImages = 1
videoLength = 5 #s

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
 

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = MyPiVideoStream((600, 208), 90)
vs.start()
time.sleep(2.0)
fps = FPS().start()
i = 0;
deadline = time.time() + videoLength
print("start time: ", time.time() )
print("deadline:   ", deadline )
# loop over some frames...this time using the threaded stream
while True: #fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF	
	
	if key == ord("q"):
            break

	if key == ord("c"):
            i = i + 1
            basePath = "/home/pi/projects/pythonEvaluation/images/pic_"
            path = basePath + str( i ) + ".png"
            cv2.imwrite( path, frame )
            
	# update the FPS counter
	fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()