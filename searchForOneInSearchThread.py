# import the necessary packages
from __future__ import print_function
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
from camera_threaded import MyPiVideoStream
from searchTemplate_thread import MyTemplateSearcher
import argparse
import imutils
import time
import cv2

display = 0
safeImages = 0
videoLength = 5 #ms

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
 

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter

mts = MyTemplateSearcher()
time.sleep(2.0)
fps = FPS().start()
i = 0;

template = cv2.imread('template_one.png')
w, h = template.shape[::2]
template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
text = "Trefferwahrscheinlichkeit: "
method = cv2.TM_CCOEFF_NORMED
deadline = time.time() + videoLength
print("start time: ", time.time() )
print("deadline:   ", deadline )
# loop over some frames using the threaded stream
mts.start()
while deadline > time.time():
    frame = mts.read()
    if frame != None:
        i = i + 1
        basePath = "/home/pi/projects/pythonEvaluation/images/pic_"
        path = basePath + str( i ) + ".jpg"
        cv2.imwrite( path, frame )
    # check to see if the frame should be displayed to our screen
    if display > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
	# update the FPS counter
    fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
mts.stop()