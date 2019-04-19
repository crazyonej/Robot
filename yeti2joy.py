#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import os
import sys
import pygame
#import ZeroBorg

# Re-direct our output to standard error, we need to ignore standard out to hide some nasty print statements from pygame
sys.stdout = sys.stderr

# Settings for the joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped	
axisLeftRight = 2                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
buttonResetEpo = 3                      # Joystick button number to perform an EPO reset (Start)
slowFactor = 0.5                        # Speed to slow to when the drive slowly button is held, e.g. 0.5 would be half speed
buttonFastTurn = 9                      # Joystick button number for turning fast (R2)
interval = 0.00                         # Time between updates in seconds, smaller responds faster but uses more processor time

# Setup pygame and wait for the joystick to become available
os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
pygame.init()
#pygame.display.set_mode((1,1))
print ('Waiting for joystick... (press CTRL+C to abort)')
while True:
	try:
		try:
			pygame.joystick.init()
			# Attempt to setup the joystick
			if pygame.joystick.get_count() < 1:
				# No joystick attached, toggle the LED
				pygame.joystick.quit()
				time.sleep(0.1)
			else:
				# We have a joystick, attempt to initialise it!
				joystick = pygame.joystick.Joystick(0)
				break
		except pygame.error:
			# Failed to connect to the joystick, toggle the LED
			pygame.joystick.quit()
			time.sleep(0.1)
	except KeyboardInterrupt:
		# CTRL+C exit, give up
		print ('User aborted')
		sys.exit()
print ('Joystick found')
joystick.init()

try:
	print ('Press CTRL+C to quit')
	driveLeft = 0.0
	driveRight = 0.0
	running = True
	hadEvent = False
	upDown = 0.0
	leftRight = 0.0
	# Loop indefinitely
	while running:
		# Get the latest events from the system
		hadEvent = False
		events = pygame.event.get()
		# Handle each event individually
		for event in events:
			if event.type == pygame.QUIT:
				# User exit
				running = False
			elif event.type == pygame.JOYBUTTONDOWN:
				# A button on the joystick just got pushed down
				#print("Joy Btn", pygame.get.button())
				#print(pygame.key.get_pressed())
				#print(event.dict, event.joy, event.button, 'pressed')
				hadEvent = True
			elif event.type == pygame.JOYAXISMOTION:
				# A joystick has been moved
				hadEvent = True
			
			if hadEvent:
				# Read axis positions (-1 to +1)
				if axisUpDownInverted:
					upDown = -joystick.get_axis(axisUpDown)
					leftRight = -joystick.get_axis(axisLeftRight)
					#print("Joy Down")
				else:
					upDown = joystick.get_axis(axisUpDown)
					leftRight = joystick.get_axis(axisLeftRight)
					#print("Joy Up")
				
				if axisLeftRightInverted:
					leftRight = -joystick.get_axis(axisLeftRight)
					#print("Joy Left")
				else:
					leftRight = joystick.get_axis(axisLeftRight)
					#print("Joy Right")
				# Apply steering speeds
				if not joystick.get_button(buttonFastTurn):
					leftRight *= 0.5
					
				# Determine the drive power levels
				if upDown < -0.05:
					# Turning left
					driveLeft *= 1.0 + (2.0 * leftRight)
					print("Joy Up")
				elif upDown > 0.05:
					# Turning right
					driveRight *= 1.0 - (2.0 * leftRight)
					print("Joy Down")
				if leftRight < -0.05:
					# Turning left
					driveLeft *= 1.0 + (2.0 * leftRight)
					print("Joy Turn Left")
				elif leftRight > 0.05:
					# Turning right
					driveRight *= 1.0 - (2.0 * leftRight)
					print("Joy Turn Right")
					
				# Check for button presses
		
				if joystick.get_button(0):
					print("Button00 A")
				elif joystick.get_button(1):
					print("Button01 B")
				elif joystick.get_button(2):
					print("Button02 ")
				elif joystick.get_button(3):
					print("Button03 X")
				elif joystick.get_button(4):
					print("Button04 Y")
				elif joystick.get_button(5):
					print("Button05")
				elif joystick.get_button(6):
					print("Button06 L1")
				elif joystick.get_button(7):
					print("Button07 R1")
				elif joystick.get_button(8):
					print("Button08 L2")
				elif joystick.get_button(9):
					print("Button09 R2")
				elif joystick.get_button(10):
					print("Button10 Select")
				elif joystick.get_button(11):
					print("Button11 Start")
					sys.exit()
					
		# Change the LED to reflect the status of the EPO latch

		# Wait for the interval period
		time.sleep(interval)
	# Disable all drives
	Print("Stop")
except KeyboardInterrupt:
	# CTRL+C exit, disable all drives
	print('Print Exit')