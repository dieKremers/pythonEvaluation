import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

while True:
    if( GPIO.input(4) == 1 ):
        ##time.sleep(0.5)
        print ("Lichtschranke verdeckt")
        
 
