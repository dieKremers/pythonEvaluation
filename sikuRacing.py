##from soundplayer import Soundplayer
from camera_threaded import MyPiVideoStream
import RPi.GPIO as GPIO
import pygame
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
RECEIVER_PIN = 4
basePath = "/home/pi/projects/pythonEvaluation/images/"
startTrigger = "/home/pi/projects/pythonEvaluation/images/start_race.txt"
qualifyingTrigger = "/home/pi/projects/pythonEvaluation/images/start_qualifying.txt"
finishPicture = "finished"

def play_startRace():
    pygame.mixer.init()
    pygame.mixer.music.load("./sounds/beep-02.wav")
    for j in range(0, 5):
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        time.sleep(1)
    pygame.mixer.music.load("./sounds/beep-01a.wav")
    createStartPicture()
    pygame.mixer.music.play()
##    while pygame.mixer.music.get_busy() == True:
##        continue
        
def play_RaceOver():
    pygame.mixer.music.load("./sounds/beep-09.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def callback_func_covered(channel):
    if GPIO.input(channel):
        global capture
        capture = True
    else:
        time.sleep(0.05)
        capture = False

def qualifyingCallback(channel):
    if GPIO.input(channel):
        global startTime
        global isqualifying
        global soundplayer
        global finishTime
        if ((time.time() - startTime)>4):
            isqualifying = False
            finishTime = time.time()

def createStartPicture():
    global startTime
    startTime = time.time()
    path = basePath + "startTime_" + str(startTime) + ".png"
    os.mknod(path)

def run():
##    vs.start()
    play_startRace()
    # loop over some frames...this time using the threaded stream
    while True: 
            # grab the frame from the threaded video stream
            frame = vs.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            picTime = time.time()
            if ( capture ): ##set True and False in GPIO Callback
                timeString = "%.3f" % (picTime)
                path = basePath + "pic_" + timeString + ".png"
                cv2.imwrite( path, frame )
            if not os.path.isfile(startTrigger):
                break

    play_RaceOver()

#-------- Main Program -----------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
    
GPIO.setup(RECEIVER_PIN, GPIO.IN)

vs.start()

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
        play_startRace()
        isqualifying = True
        while isqualifying:
            time.sleep(0.1)
        play_RaceOver()
        path = basePath + finishPicture + "_" + str(finishTime) + ".png"
        os.mknod(path)
        GPIO.remove_event_detect(RECEIVER_PIN)
        print("... Qualifying over")

print("das war's")
vs.stop()
GPIO.remove_event_detect(RECEIVER_PIN)
