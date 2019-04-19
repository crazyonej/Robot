#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# @reboot sleep 5 && /bin/echo -e 'connect 85:55:A2:70:33:B3 \n quit \n' | bluetoothctl
# Distributed under terms of the MIT license.

import os
import pprint
import pygame
import RPi.GPIO as GPIO

M1a = 4
M1b = 17
M2a	= 27
M2b = 22

Led1 = 7
Led2 = 8

#Right
LedBD0 = 18
LedBD1 = 25

BtnBlue = 23
BtnRed	= 24

en1  = 9
en2  = 10
spd  = 50

sensor1LED = 20
Fire = 21

AutoMode = 26
KillSwitch = 19
Killing = False

DepthTrig = 5
DepthEcho = 6

GPIO.setmode(GPIO.BCM)

print("init")
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.setup(BtnBlue,GPIO.IN)
GPIO.setup(BtnRed,GPIO.IN)

GPIO.setup(BtnBlue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BtnRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.setup(M1a, GPIO.OUT)
GPIO.setup(M1b, GPIO.OUT)
GPIO.setup(M2a, GPIO.OUT)
GPIO.setup(M2b, GPIO.OUT)
GPIO.setup(Led1,GPIO.OUT)
GPIO.setup(Led2,GPIO.OUT)
GPIO.setup(LedBD0,GPIO.OUT)
GPIO.setup(LedBD1,GPIO.OUT)
GPIO.setup(sensor1LED, GPIO.OUT)
GPIO.setup(Fire, GPIO.OUT)

GPIO.setup(DepthTrig,GPIO.OUT)
GPIO.setup(DepthEcho,GPIO.IN)
GPIO.setup(BtnBlue,GPIO.IN)
GPIO.setup(BtnRed,GPIO.IN)

GPIO.setup(AutoMode, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KillSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(BtnBlue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BtnRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(LedBD0,True)		# LED Off
GPIO.output(LedBD1,False)		# LED Off

p1=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)
p1.start(50)
p2.start(50)
	
def init():
	print("init")
	GPIO.setup(BtnBlue,GPIO.IN)
	GPIO.setup(BtnRed,GPIO.IN)

	GPIO.setup(BtnBlue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BtnRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	
	GPIO.setup(M1a, GPIO.OUT)
	GPIO.setup(M1b, GPIO.OUT)
	GPIO.setup(M2a, GPIO.OUT)
	GPIO.setup(M2b, GPIO.OUT)
	GPIO.setup(Led1,GPIO.OUT)
	GPIO.setup(Led2,GPIO.OUT)
	GPIO.setup(LedBD0,GPIO.OUT)
	GPIO.setup(LedBD1,GPIO.OUT)
	GPIO.setup(sensor1LED, GPIO.OUT)
	GPIO.setup(Fire, GPIO.OUT)
	
	GPIO.setup(DepthTrig,GPIO.OUT)
	GPIO.setup(DepthEcho,GPIO.IN)
	GPIO.setup(BtnBlue,GPIO.IN)
	GPIO.setup(BtnRed,GPIO.IN)

	GPIO.setup(AutoMode, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(KillSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	GPIO.setup(BtnBlue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BtnRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	GPIO.output(LedBD0,True)		# LED Off
	GPIO.output(LedBD1,False)		# LED Off
	
	p1=GPIO.PWM(en1,1000)
	p2=GPIO.PWM(en2,1000)
	p1.start(50)
	p2.start(50)

def sRange(val):
	OldRange = (100 - 0)
	
	if (OldRange == 0):
		NewValue = 50
		spd = round(NewValue, 0)
	else:
		NewRange = (100 - 50)  
		NewValue = (((val - 0) * NewRange) / OldRange) + 50
	
	spd = round(NewValue, 0)
	print("DutyCycle", spd)
	p1.ChangeDutyCycle(spd)
	p2.ChangeDutyCycle(spd)
	#return NewValue
	
	
def MoveForward(tf):
	print("forward")
	GPIO.output(M1a,True)
	GPIO.output(M1b,False)
	GPIO.output(M2a,True)
	GPIO.output(M2b,False)

	
def MoveBack(tf):
	print("back") 
	GPIO.output(M1a,False)
	GPIO.output(M1b,True)
	GPIO.output(M2a,False)
	GPIO.output(M2b,True)


def MoveLeft(tf):
	print("left")
	GPIO.output(M1a,True)
	GPIO.output(M1b,False)
	GPIO.output(M2a,False)
	GPIO.output(M2b,True)


def MoveRight(tf):
	print("right")
	GPIO.output(M1a,False)
	GPIO.output(M1b,True)
	GPIO.output(M2a,True)
	GPIO.output(M2b,False)


def stop(): 
	print("Stop") 
	GPIO.output(M1a,False)
	GPIO.output(M1b,False)
	GPIO.output(M2a,False)
	GPIO.output(M2b,False)

def FireIt():
	GPIO.output(Fire,True)
	time.sleep(1.5)
	GPIO.output(Fire,False)

def SySQuit():
	print("System Quit")
	GPIO.output(Led1,False)
	GPIO.output(Led2,False)
	stop()
	BDDisConnect()
	GPIO.cleanup()

	
class PS4Controller(object):
	"""Class representing the PS4 controller. Pretty straightforward functionality."""

	controller = None
	axis_data = None
	button_data = None
	hat_data = None

	def init(self):
		"""Initialize the joystick components"""
		
		os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
		pygame.init()
		
		pygame.joystick.init()
		
		self.controller = pygame.joystick.Joystick(0)
		self.controller.init()
		
		#init()

	def listen(self):
		"""Listen for events to happen"""
		
		if not self.axis_data:
			self.axis_data = {}

		if not self.button_data:
			self.button_data = {}
			for i in range(self.controller.get_numbuttons()):
				self.button_data[i] = False

		if not self.hat_data:
			self.hat_data = {}
			for i in range(self.controller.get_numhats()):
				self.hat_data[i] = (0, 0)

		while True:
			for event in pygame.event.get():
				if event.type == pygame.JOYAXISMOTION:
					#if (event.axis == 0) and 
					if event.axis == 0:
						print("val-", event.value)
						print("spd", abs(event.value) *100)
						#Range(abs(event.value) *100)
						if event.value > 0:
							print ("right")
							MoveRight(0)
						if event.value < 0:
							print ("left")
							MoveLeft(0)
						else:
							print("stop RtLf")
							stop()
					if event.axis == 1:
						print("val-", event.value)
						print("spd", abs(event.value) *100)
						sRange(abs(event.value) *100)
						if event.value > 0:
							print ("down")
							MoveBack(0)
						if event.value < 0:
							print ("up")
							MoveForward(0)
						else:
							print("stop UpDn")
							stop()
					
					if event.axis == 2:
						print("val-", event.value)
						print("spd", abs(event.value) *100)
						if event.value > 0:
							print ("Cam right")
						if event.value < 0:
							print ("Cam left")
					if event.axis == 3:
						print("val-", event.value)
						print("spd", abs(event.value) *100)
						if event.value > 0:
							print ("Cam down")
						if event.value < 0:
							print ("Cam up")
							
				elif event.type == pygame.JOYHATMOTION:
					if event.hat == 0:
						if event.value == (1, 0):
							print ("Hat right")
							MoveRight(0)
						elif event.value == (-1, 0):
							print ("Hat left")
							MoveLeft(0)
						elif event.value == (0, 1):
							print ("Hat up")
							MoveForward(0)
						elif event.value == (0, -1):
							print ("Hat down")
							MoveBack(0)
						else:
							print("stop Hat")
							stop()

				elif event.type == pygame.JOYBUTTONDOWN:
					print("Joy Btn-", event.button)
					
					if event.button == 0:
						print ("Button01 A")
					elif event.button == 1:
						print("Button01 B")
						FireIt()
					elif event.button == 2:
						print("Button02 ")
					elif event.button == 3:
						print("Button03 X")
						stop()
					elif event.button == 4:
						print("Button04 Y")
					elif event.button == 5:
						print("Button05")
					elif event.button == 6:
						print("Button06 L1")
					elif event.button == 7:
						print("Button07 R1")
					elif event.button == 8:
						print("Button08 L2")
						stop()
					elif event.button == 9:
						print("Button09 R2")
						stop()
					elif event.button == 10:
						print("Button10 Select")
					elif event.button == 11:
						print("Button11 Start")
						SySQuit()
					elif event.button == 13:
						print("Button13 JoyL")
					elif event.button == 14:
						print("Button14 JoyR")

				elif event.type == pygame.JOYBUTTONUP:
					if event.button == 2:
						print ("he-yump")
				
				else:
					print("stop")
					
			if (GPIO.input(BtnBlue) == False):
				print("Btn Blue")
				#BDConnect()
			if (GPIO.input(BtnRed) == False):
				print("Btn Red")
		
		if (GPIO.input(BtnBlue) == False):
				print("Btn Blue2")
				#BDConnect()
		if (GPIO.input(BtnRed) == False):
			print("Btn Red2")
				
if __name__ == "__main__":
	ps4 = PS4Controller()
	ps4.init()
	ps4.listen()