import pygame
import time

class Soundplayer:
    def play_startRace():
        pygame.mixer.init()
        pygame.mixer.music.load("./sounds/beep-02.wav")
        for j in range(0, 5):
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            time.sleep(1)
        pygame.mixer.music.load("./sounds/beep-01a.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        
    def play_RaceOver():
        pygame.mixer.music.load("./sounds/beep-09.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
