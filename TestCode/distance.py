#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import threading
from sensor import distance

PIN_TRIGGER = 5
PIN_ECHO = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

def Dis():
	GPIO.output(PIN_TRIGGER, GPIO.LOW)
	print ("Waiting for sensor to settle")
	time.sleep(0.25)
	print ("Calculating distance")
	GPIO.output(PIN_TRIGGER, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(PIN_TRIGGER, GPIO.LOW)
	
def check_front():
    init()
    dist = distance()

    if dist < 25:
        print('Too close,',dist)
        init()
        reverse(2)
        dist = distance()
        if dist < 25:
            print('Too close,',dist)
            init()
            pivot_left(3)
            init()
            reverse(2)
            dist = distance()
            if dist < 25:
                print('Too close, giving up',dist)
                sys.exit()


def autonomy():
    tf = 0.030
    x = random.randrange(0,4)

    if x == 0:
        for y in range(30):
            check_front()
            init()
            forward(tf)
    elif x == 1:
        for y in range(30):
            check_front()
            init()
            pivot_left(tf)
    elif x == 2:
        for y in range(30):
            check_front()
            init()
            turn_right(tf)
    elif x == 3:
        for y in range(30):
            check_front()
            init()
            turn_left(tf)

for z in range(10):
    autonomy()	
	
try:
	while True:
		
		threading.Timer(3.0, Dis).start()
		
		while GPIO.input(PIN_ECHO)==0:
			pulse_start_time = time.time()
		while GPIO.input(PIN_ECHO)==1:
			pulse_end_time = time.time()

		pulse_duration = pulse_end_time - pulse_start_time
		
		distance = round(pulse_duration * 17150, 2)
		
		print ("Distance:",distance,"cm")

finally:
      GPIO.cleanup()