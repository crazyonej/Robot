import RPi.GPIO as GPIO
import curses  
from time import sleep

in1 = 4
in2 = 17
in3 = 27
in4 = 22

en1  = 9
en2  = 10
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p1=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)
p1.start(50)
p2.start(50)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

while(1):

	#x=raw_input()
	x=screen.getch()
	
	if x==ord('r'):
		print("run")
		if(temp1==1):
			GPIO.output(in1,GPIO.HIGH)
			GPIO.output(in2,GPIO.LOW)
			GPIO.output(in3,GPIO.HIGH)
			GPIO.output(in4,GPIO.LOW)
			print("forward")
			x='z'
		else:
			GPIO.output(in1,GPIO.LOW)
			GPIO.output(in2,GPIO.HIGH)
			print("backward")
			x='z'


	elif x==ord('s'):
		print("stop")
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.LOW)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.LOW)
		x='z'

	elif x==ord('f'):
		print("forward")
		GPIO.output(in1,GPIO.HIGH)
		GPIO.output(in2,GPIO.LOW)
		GPIO.output(in3,GPIO.HIGH)
		GPIO.output(in4,GPIO.LOW)
		temp1=1
		x='z'

	elif x==ord('b'):
		print("backward")
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.HIGH)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.HIGH)
		temp1=0
		x='z'

	elif x==ord('l'):
		print("low")
		p1.ChangeDutyCycle(50)
		p2.ChangeDutyCycle(50)
		x='z'

	elif x==ord('m'):
		print("medium")
		p1.ChangeDutyCycle(75)
		p2.ChangeDutyCycle(75)
		x='z'

	elif x==ord('h'):
		print("high")
		p1.ChangeDutyCycle(100)
		p2.ChangeDutyCycle(100)
		x='z'
		
	elif x==ord('e'):
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()
		GPIO.cleanup()
		break
	
	else:
		print("<<<  wrong data  >>>")
		print("please enter the defined data to continue.....")