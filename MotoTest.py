
import RPi.GPIO as GPIO
import time #import time module

M1a = 4
M1b = 17
M2a	= 27
M2b = 22

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1a,GPIO.OUT)
GPIO.setup(M1b,GPIO.OUT)
GPIO.setup(M2a,GPIO.OUT)
GPIO.setup(M2b,GPIO.OUT)

GPIO.output(M1a,True)
time.sleep(1)
GPIO.output(M1a,False)
GPIO.output(M1b,True)
time.sleep(1)
GPIO.output(M1b,False)
GPIO.output(M2a,True)
time.sleep(1)
GPIO.output(M2a,False)
GPIO.output(M2b,True)
time.sleep(1)
GPIO.output(M2b,False)