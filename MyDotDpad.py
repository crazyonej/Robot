#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os #added so we can shut down OK
import time #import time module
from bluedot import BlueDot
from signal import pause

M1a = 4
M1b = 17
M2a	= 27
M2b = 22

Led1 = 18
Led2 = 23
Fire = 21

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1a,GPIO.OUT)
GPIO.setup(M1b,GPIO.OUT)
GPIO.setup(M2a,GPIO.OUT)
GPIO.setup(M2b,GPIO.OUT)

GPIO.setup(Led1,GPIO.OUT)
GPIO.setup(Led2,GPIO.OUT)

sensor = 24
sled = 26
sleeptime = 0.1

GPIO.setup(sensor, GPIO.IN)
GPIO.setup(sled, GPIO.OUT)
GPIO.setup(Fire, GPIO.OUT)

for x in range(1, 10):
		GPIO.output(Led1,False)
		GPIO.output(Led2,False)
		time.sleep(.5)
		GPIO.output(Led1,True)
		GPIO.output(Led2,True)
		time.sleep(1)	

def FireIt():
	GPIO.output(Fire,True)
	time.sleep(1.5)
	GPIO.output(Fire,False)
		
def dpad(pos):
	if pos.top: 
		print("up")
		GPIO.output(M1a,True)
		GPIO.output(M1b,False)
		GPIO.output(M2a,True)
		GPIO.output(M2b,False)
	elif pos.bottom:
		print("down") 
		GPIO.output(M1a,False)
		GPIO.output(M1b,True)
		GPIO.output(M2a,False)
		GPIO.output(M2b,True)
	elif pos.left:
		print("left")
		GPIO.output(M1a,True)
		GPIO.output(M1b,False)
		GPIO.output(M2a,False)
		GPIO.output(M2b,True)
	elif pos.right:
		print("right")
		GPIO.output(M1a,False)
		GPIO.output(M1b,True)
		GPIO.output(M2a,True)
		GPIO.output(M2b,False)
	elif pos.middle: 
		print("fire")
		FireIt()

def stop(): 
	print("Stop") 
	GPIO.output(M1a,False)
	GPIO.output(M1b,False)
	GPIO.output(M2a,False)
	GPIO.output(M2b,False)

def quit():
	if(pos.middle):
		print("just fire")
	else:
		print("Quit")
	#os.system ('sudo shutdown now') # shutdown right now!
	#break
	
try:
	while True:
		bd = BlueDot() 
		bd.when_pressed = dpad
		bd.when_moved = dpad 
		bd.when_released = stop
		#bd.when_double_pressed = quit
		
		if (GPIO.input(sensor) == True):
			print('Sensor True')
			GPIO.output(sled, False)
		else:
			print('Sensor False')
			GPIO.output(sled, True)
			
		pause()
finally:
	#Close down curses properly, inc turn echo back on!
	GPIO.cleanup()
