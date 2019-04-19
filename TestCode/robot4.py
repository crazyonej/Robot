#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os #added so we can shut down OK
import time #import time module
from bluedot import BlueDot
from signal import pause
#import threading
import random

M1a = 4
M1b = 17
M2a	= 27
M2b = 22

Led1 = 18
Led2 = 23
Fire = 21

AutoMode = 26

sensor1LED = 20

DepthTrig = 5
DepthEcho = 6

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1a,GPIO.OUT)
GPIO.setup(M1b,GPIO.OUT)
GPIO.setup(M2a,GPIO.OUT)
GPIO.setup(M2b,GPIO.OUT)

GPIO.setup(Led1,GPIO.OUT)
GPIO.setup(Led2,GPIO.OUT)

sleeptime = 0.1

GPIO.setup(sensor1LED, GPIO.OUT)

GPIO.setup(Fire, GPIO.OUT)

GPIO.setup(DepthTrig,GPIO.OUT)
GPIO.setup(DepthEcho,GPIO.IN)
#GPIO.setup(AutoMode,GPIO.IN)
GPIO.setup(AutoMode, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for x in range(1, 5):
	print("Booting:{0}" .format(x))
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

def init():
	#gpio.setmode(gpio.BCM)
	GPIO.setup(M1a, GPIO.OUT)
	GPIO.setup(M1b, GPIO.OUT)
	GPIO.setup(M2a, GPIO.OUT)
	GPIO.setup(M2b, GPIO.OUT)

def MoveForward(tf):
	print("forward")
	GPIO.output(M1a,True)
	GPIO.output(M1b,False)
	GPIO.output(M2a,True)
	GPIO.output(M2b,False)
	#if(AutoMode):
	#	time.sleep(tf)
		#stop()
	
def MoveBack(tf):
	print("back") 
	GPIO.output(M1a,False)
	GPIO.output(M1b,True)
	GPIO.output(M2a,False)
	GPIO.output(M2b,True)
	if(AutoMode):
		time.sleep(tf)
		#stop()

def MoveLeft(tf):
	print("left")
	GPIO.output(M1a,True)
	GPIO.output(M1b,False)
	GPIO.output(M2a,False)
	GPIO.output(M2b,True)
	if(AutoMode):
		time.sleep(tf)
		#stop()

def MoveRight(tf):
	print("right")
	GPIO.output(M1a,False)
	GPIO.output(M1b,True)
	GPIO.output(M2a,True)
	GPIO.output(M2b,False)
	if(AutoMode):
		time.sleep(tf)
		#stop()
	
def dpad(pos):
	if pos.top: 
		print("up")
		MoveForward(0)
	elif pos.bottom:
		print("down") 
		MoveBack(0)
	elif pos.left:
		print("left")
		MoveLeft(0)
	elif pos.right:
		print("right")
		MoveRight(0)
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

def distance():
	# set Trigger to HIGH
	GPIO.output(DepthTrig, True)
	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(DepthTrig, False)

	StartTime = time.time()
	StopTime = time.time()

	while GPIO.input(DepthEcho) == 0:
		StartTime = time.time()
	while GPIO.input(DepthEcho) == 1:
		StopTime = time.time()

	TimeElapsed = StopTime - StartTime

	space = (TimeElapsed * 34300) / 2
	
	print ("Distance:",space,"cm")
	
	check_front(space)
	#return distance

def check_front(dist):
	#stop()
	#print ("CheckDistance:",dist)

	if int(dist) < 25:
		print('Too close,',dist)
		#stop()
		MoveBack(3)
		
		if int(dist) < 25:
			print('Too close,',dist)
			#stop()
			MoveLeft(3)
			#stop()
			#MoveBack(2)
			if dist < 25:
				print('Too close, giving up',dist)
				stop()
				#sys.exit()

def autonomy():
	tf = 0.030
	x = random.randrange(0,4)

	if x == 0:
		for y in range(30):
			distance()
			MoveForward(tf)
	elif x == 1:
		for y in range(30):
			distance()
			MoveLeft(tf)
	elif x == 2:
		for y in range(30):
			distance()
			MoveRight(tf)
	elif x == 3:
		for y in range(30):
			distance()
			MoveLeft(tf)


if (GPIO.input(AutoMode) == False):
	print("AutoMode")
else:
	print("NormalMode")
		
try:
	while True:
		if (GPIO.input(AutoMode) == False):
			tf = 5
			distance()
			MoveForward(tf)
			#for z in range(10):
			#	autonomy()
			#time.sleep(2)
	
		else:
			
			bd = BlueDot() 
			bd.when_pressed = dpad
			bd.when_moved = dpad 
			bd.when_released = stop()
			#bd.when_double_pressed = quit
				
			pause()
finally:
	#Close down curses properly, inc turn echo back on!
	GPIO.cleanup()