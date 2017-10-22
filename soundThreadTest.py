from soundplayThreaded import MyPiSoundplayer
import time

soundplayer = MyPiSoundplayer()
soundplayer.start()
soundplayer.playStart()
soundplayer.playStop()

while soundplayer.isActive() == True:
    time.sleep(0.1)
    
soundplayer.stop()
