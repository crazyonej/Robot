import RPi.GPIO as GPIO
import os
from time import sleep
from subprocess import call
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)
flag = 0
try:  
    while True:             
        if GPIO.input(32) != 1: # if port 25 == 1  
            sleep(0.5)
            if flag == 0:
              print "Sending Stream"  
              
              os.system("raspivid -n -t 0 -md 2 -fps 30 -vf -hf -o /media/DEVICE/$(date +'%Y-%m-%d_%H%M%S').h264 &")
              flag = 1
            
            elif flag == 1:
              print "Stopping Stream"
              call (["pkill raspivid"], shell=True)
              os.system("sync")
              flag = 0
            
        sleep(0.05)         # wait 0.1 seconds  
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup() 
