# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import os #added so we can shut down OK
from time import sleep

Pan = 14
Tilt = 15

SetPan = 90
SetTilt = 90

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(Pan,GPIO.OUT)
GPIO.setup(Tilt,GPIO.OUT)

sleeptime = 0.1

pwm1=GPIO.PWM(Pan,50)
pwm2=GPIO.PWM(Tilt,50)
pwm1.start(7)
pwm2.start(7)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

def setServoAngle(servo, angle):
	#assert angle >=30 and angle <= 150
	assert angle >=10 and angle <= 220
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	time.sleep(0.3)
	pwm.stop()

	
def TestServo():
	for i in range(0,180):
		DC=1./18.*(i)+2
		pwm1.ChangeDutyCycle(DC)
		time.sleep(.02)
	for i in range(180,0,-1):
		DC=1/18.*i+2
		pwm1.ChangeDutyCycle(DC)
		time.sleep(.02)

def TestServo2(range):
	pwm1.start(8)
	DC = 1./18.*(range)+2
	pwm1.ChangeDutyCycle(DC)
	time.sleep(0.3)
	pwm1.stop()

		
try:
		while True:
			
			char = screen.getch()
			if char == ord('q'):
				break
			if char == ord('S'): # Added for shutdown on capital S
				os.system ('sudo shutdown now') # shutdown right now!
			elif char == curses.KEY_UP:
				print("Key Up\r")
				#setServoAngle(pan, int(sys.argv[1])) # 30 ==> 90 (middle point) ==> 150
				SetTilt += 5
				print("SetPan {}\r".format(SetTilt))
				TestServo2(SetTilt)
				#setServoAngle(Pan, SetTilt)
			elif char == curses.KEY_DOWN:
				print("Key Dn\r")
				SetTilt -= 5
				print("SetPan {}\r".format(SetTilt))
				TestServo2(SetTilt)
				#setServoAngle(Pan, SetTilt)
			elif char == curses.KEY_RIGHT:
				print("Key Right\r")
				#setServoAngle(tilt, int(sys.argv[2])) # 30 ==> 90 (middle point) ==> 150
				SetPan += 5
				print("SetPan {}\r".format(SetPan))
				TestServo2(SetPan)
				#setServoAngle(Tilt, SetPan)
			elif char == curses.KEY_LEFT:
				print("Key Left\r")
				SetPan -= 5
				print("SetPan {}\n".format(SetPan))
				TestServo2(SetPan)
				#setServoAngle(Tilt, SetPan)
			else:
				print ('char:', char)
			time.sleep(0.5)

finally:
	#Close down curses properly, inc turn echo back on!
	curses.nocbreak(); screen.keypad(0); curses.echo()
	curses.endwin()
	pwm1.stop()
	pwm2.stop()
	GPIO.cleanup()