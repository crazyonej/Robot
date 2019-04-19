# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import os #added so we can shut down OK
import time #import time module

M1a = 4

M1b = 17
M2a	= 27
M2b = 22
Led	= 18

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1a,GPIO.OUT)
GPIO.setup(M1b,GPIO.OUT)
GPIO.setup(M2a,GPIO.OUT)
GPIO.setup(M2b,GPIO.OUT)
GPIO.setup(Led,GPIO.OUT)


sensor = 24
sled = 26
sleeptime = 0.1

GPIO.setup(sensor, GPIO.IN)
GPIO.setup(sled, GPIO.OUT)

for x in range(1, 10):
		GPIO.output(Led,False)
		time.sleep(.5)
		GPIO.output(Led,True)
		time.sleep(1)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

try:
		while True:
			if (GPIO.input(sensor) == True):
				print('Sensor True')
				GPIO.output(sled, False)
			else:
				print('Sensor False')
				GPIO.output(sled, True)
			
			char = screen.getch()
			if char == ord('q'):
				break
			if char == ord('S'): # Added for shutdown on capital S
				os.system ('sudo shutdown now') # shutdown right now!
			elif char == curses.KEY_UP:
				print'Key Up\n'
				GPIO.output(M1a,True)
				GPIO.output(M1b,False)
				GPIO.output(M2a,True)
				GPIO.output(M2b,False)
			elif char == curses.KEY_DOWN:
				print'Key Dn\n'
				GPIO.output(M1a,False)
				GPIO.output(M1b,True)
				GPIO.output(M2a,False)
				GPIO.output(M2b,True)
			elif char == curses.KEY_RIGHT:
				print'Key Right\n'
				GPIO.output(M1a,False)
				GPIO.output(M1b,True)
				GPIO.output(M2a,True)
				GPIO.output(M2b,False)
			elif char == curses.KEY_LEFT:
				print'Key Left\n'
				GPIO.output(M1a,True)
				GPIO.output(M1b,False)
				GPIO.output(M2a,False)
				GPIO.output(M2b,True)
			elif char == 10:
				print'stop\n'
				GPIO.output(M1a,False)
				GPIO.output(M1b,False)
				GPIO.output(M2a,False)
				GPIO.output(M2b,False)
			else:
				print ('char:', char)

finally:
	#Close down curses properly, inc turn echo back on!
	curses.nocbreak(); screen.keypad(0); curses.echo()
	curses.endwin()
	GPIO.cleanup()