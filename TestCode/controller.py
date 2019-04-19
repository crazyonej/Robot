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
						if event.value > 0:
							print ("right")
						if event.value < 0:
							print ("left")
					if event.axis == 1:
						if event.value > 0:
							print ("down")
						if event.value < 0:
							print ("up")
					
					if event.axis == 2:
						if event.value > 0:
							print ("Cam right")
						if event.value < 0:
							print ("Cam left")
					if event.axis == 3:
						if event.value > 0:
							print ("Cam down")
						if event.value < 0:
							print ("Cam up")
							
				elif event.type == pygame.JOYBUTTONDOWN:
					if event.button == 1:
						print ("wow pressed the X button")
				elif event.type == pygame.JOYBUTTONUP:
					if event.button == 1:
						print ("he-yump")
				elif event.type == pygame.JOYHATMOTION:
					if event.hat == 0:
						if event.value == (1, 0):
							print ("Hat right")
						if event.value == (-1, 0):
							print ("Hat left")
						if event.value == (0, 1):
							print ("Hat up")
						if event.value == (0, -1):
							print ("Hat down")


if __name__ == "__main__":
	ps4 = PS4Controller()
	ps4.init()
	ps4.listen()