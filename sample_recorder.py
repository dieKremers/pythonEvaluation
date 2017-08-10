# import the necessary packages
##from __future__ import print_function
##from picamera.array import PiRGBArray
##from picamera import PiCamera
from soundplayer import Soundplayer
from camera_threaded import MyPiVideoStream
import RPi.GPIO as GPIO
##import argparse
##import imutils
import os
import time
import cv2

display = 0
videoLength = 10 #s
capture = False
isqualifying = False
startTime = 0
finishTime = 0
vs = MyPiVideoStream((608, 208), 90)
soundplayer = Soundplayer
RECEIVER_PIN = 4
basePath = "/home/pi/projects/pythonEvaluation/images/"
startTrigger = "/home/pi/projects/pythonEvaluation/images/start_race.txt"
qualifyingTrigger = "/home/pi/projects/pythonEvaluation/images/start_qualifying.txt"
finishPicture = "finished"
 
def callback_func_covered(channel):
    if GPIO.input(channel):
        ##time.sleep(0.025)
        global capture
        ##print ("Rising Edge Detected at ", time.time() )
        capture = True
    else:
        time.sleep(0.1)
        capture = False
        ##print ("Falling Edge Detected at ", str(time.time()) )

def qualifyingCallback(channel):
    if GPIO.input(channel):
        global startTime
        global isqualifying
        global soundplayer
        global finishTime
        if ((time.time() - startTime)>2.5):
            isqualifying = False
            finishTime = time.time()

def createStartPicture():
    path = basePath + "startTime_" + str(time.time()) + ".png"
    os.mknod(path)

def run():
    vs.start()
    soundplayer.play_startRace()
    createStartPicture()
    deadline = time.time() + videoLength
    # loop over some frames...this time using the threaded stream
    while os.path.isfile(startTrigger): ##deadline > time.time():
            # grab the frame from the threaded video stream
            frame = vs.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            picTime = time.time()
            if ( capture ): ##set True and False in GPIO Callback
                timeString = "%.3f" % (picTime)
                path = basePath + "pic_" + timeString + ".png"
                cv2.imwrite( path, frame )

    soundplayer.play_RaceOver()
    vs.stop()

#-------- Main Program -----------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
    
GPIO.setup(RECEIVER_PIN, GPIO.IN)


##run()
##endless loop
while True:
    time.sleep(1)
    if os.path.isfile(startTrigger):
        print ("Starting Race ...")
        GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH, callback=callback_func_covered)
        run()
        GPIO.remove_event_detect(RECEIVER_PIN)
        print("... Race over")
    if os.path.isfile(qualifyingTrigger):
        print ("Start Qualifying...")
        os.remove( qualifyingTrigger )
        GPIO.add_event_detect(RECEIVER_PIN, GPIO.RISING, callback=qualifyingCallback)
        soundplayer.play_startRace()
        startTime = time.time()
        createStartPicture()
        isqualifying = True
        while isqualifying:
            time.sleep(0.1)
        soundplayer.play_RaceOver()
        path = basePath + finishPicture + "_" + str(finishTime) + ".png"
        os.mknod(path)
        GPIO.remove_event_detect(RECEIVER_PIN)
        print("... Qualifying over")

print("das war's")
GPIO.remove_event_detect(RECEIVER_PIN)
