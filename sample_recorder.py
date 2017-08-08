# import the necessary packages
from __future__ import print_function
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
from camera_threaded import MyPiVideoStream
import RPi.GPIO as GPIO
import argparse
import imutils
import time
import cv2
import pygame
pygame.mixer.init()
pygame.mixer.music.load("./sounds/beep-01a.wav")
display = 0
safeImages = 1
videoLength = 10 #s
capture = False
capture
vs = MyPiVideoStream((608, 208), 90)

RECEIVER_PIN = 4
 
def callback_func_covered(channel):
    if GPIO.input(channel):
        time.sleep(0.025)
        global capture
        print ("Rising Edge Detected at ", time.time() )
        capture = True
    else:
        time.sleep(0.1)
        capture = False
        print ("Falling Edge Detected at ", str(time.time()) )

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
    
GPIO.setup(RECEIVER_PIN, GPIO.IN)
GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH, callback=callback_func_covered, bouncetime=10)
##GPIO.add_event_detect(RECEIVER_PIN, GPIO.FALLING, callback=callback_func_free, bouncetime=200)

          

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

vs.start()
time.sleep(2.0)

pygame.mixer.music.load("./sounds/beep-02.wav")
for j in range(0, 1):
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    time.sleep(1)

pygame.mixer.music.load("./sounds/beep-01a.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

deadline = time.time() + videoLength
print("start time: ", time.time() )
print("deadline:   ", deadline )
fps = FPS().start()
i = 0;
basePath = "/home/pi/projects/pythonEvaluation/images/pic_"

# loop over some frames...this time using the threaded stream
while deadline > time.time(): #fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	picTime = time.time()
	if ( capture ): ##safeImages > 0:
            wasOn = True
            i = i + 1
            timeString = "%.3f" % (picTime)
            path = basePath + timeString + ".png"
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

pygame.mixer.music.load("./sounds/beep-09.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
 
# do a bit of cleanup
GPIO.remove_event_detect(RECEIVER_PIN)
cv2.destroyAllWindows()
vs.stop()