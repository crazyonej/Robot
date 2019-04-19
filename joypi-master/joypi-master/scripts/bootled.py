import RPi.GPIO as GPIO
import os
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(13, True)
try:  
    while True:
        if GPIO.input(31) != 1:  
            sleep(0.5)
            print "Shutting down"  
            os.system("halt")
        sleep(0.1)
  
finally:             
    GPIO.cleanup() 
