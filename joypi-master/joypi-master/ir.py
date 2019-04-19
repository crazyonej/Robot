import time
import signal
import pygame
import sys
import os
import RPi.GPIO as GPIO
# The following is an example code written to controll the l298n motor contoller
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN) #Front Left
GPIO.setup(8, GPIO.IN) #Front Center
GPIO.setup(10, GPIO.IN) #Front Right
GPIO.setup(23, GPIO.IN) #Back Left
GPIO.setup(24, GPIO.IN) #Back Center
GPIO.setup(26, GPIO.IN) #Back Right

while True:
  os.system('clear')
  fl = GPIO.input(7)
  print fl
  fc = GPIO.input(8)
  print fc
  fr = GPIO.input(10)
  print fr
  bl = GPIO.input(23)
  print bl
  bc = GPIO.input(24)
  print bc
  br = GPIO.input(26)
  print br
  time.sleep(0.2)
  
