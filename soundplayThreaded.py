# import the necessary packages
import pygame
import time
import os
from threading import Thread

class MyPiSoundplayer:
	def __init__(self, basePath="/home/pi/projects/pythonEvaluation/images/"): #, resolution=(800, 200), framerate=90):
		# initialize the camera and stream
		self.basePath = basePath
		self.welcomeWav = "/home/pi/projects/pythonEvaluation/sounds/im-so-ready.wav"
		self.startLowWav = "/home/pi/projects/pythonEvaluation/sounds/beep-02.wav"
		self.startHighWav = "/home/pi/projects/pythonEvaluation/sounds/beep-01a.wav"
		self.stopWav = "/home/pi/projects/pythonEvaluation/sounds/beep-09.wav"
		self.triggerStart = False
		self.triggerStop = False
		self.triggerWelcome = False
		# initialize the variable used to indicate
		# if the thread should be stopped
		self.stopped = False
		
	def start(self):
		# start the thread to read frames from the video stream
		self.stopped = False
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
                pygame.mixer.init()
                while self.stopped == False:
                    if self.triggerStart:
                        print("Play Start")
                        self.play_startRace()
                        self.triggerStart = False
                    if self.triggerStop:
                        print("Play Stop")
                        self.play_RaceOver()
                        self.triggerStop = False
                    if self.triggerWelcome:
                        print("Play Welcome")
                        self.play_Welcome()
                        self.triggerWelcome = False
                    time.sleep(0.2)
                return


	def play_startRace(self):
            pygame.mixer.music.load(self.startLowWav)
            for j in range(0, 5):
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
                time.sleep(1)
            pygame.mixer.music.load(self.startHighWav)
            self.createStartPicture()
            self.triggerStart = False
            pygame.mixer.music.play()

	def play_RaceOver(self):
            pygame.mixer.music.load(self.stopWav)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

	def play_Welcome(self):
            pygame.mixer.init()
            pygame.mixer.music.load(self.welcomeWav)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
    
	def playStart(self):
		# return the frame most recently read
		self.triggerStart = True
		return
 
	def playStop(self):
		# indicate that the thread should be stopped
		self.triggerStop = True
		return
		
	def playWelcome(self):
            self.triggerWelcome = True
            return
            
	def stop(self):
            self.stopped = True

	def isActive(self):
            if self.triggerStart == True:
                return True
            if self.triggerStop == True:
                return True
            if self.triggerWelcome == True:
                return True
            return False
        
	def createStartPicture(self):
	    startTime = time.time()
	    path = self.basePath + "startTime_" + str(startTime) + ".png"
	    os.mknod(path)