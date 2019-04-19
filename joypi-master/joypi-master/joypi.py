import time
import signal
import pygame
import sys
import RPi.GPIO as GPIO
# The following is an example code written to controll the l298n motor contoller
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) #input-1
GPIO.setup(12, GPIO.OUT) #input-2
GPIO.setup(15, GPIO.OUT) #input-3
GPIO.setup(16, GPIO.OUT) #input-4
GPIO.setup(7, GPIO.IN) #Front Left
GPIO.setup(8, GPIO.IN) #Front Center
GPIO.setup(10, GPIO.IN) #Front Right
GPIO.setup(23, GPIO.IN) #Back Left
GPIO.setup(24, GPIO.IN) #Back Center
GPIO.setup(26, GPIO.IN) #Back Right
GPIO.setup(18, GPIO.OUT)  #Status-LED
  
pygame.init()
 
done = False
# Initialize the joysticks
pygame.joystick.init()

################ Movement Definitions BEGIN #######################
def forward_left():
    print "FL"
    GPIO.output(11, False)
    GPIO.output(12, False)
    GPIO.output(16, True)
    GPIO.output(15, False)

def forward_right():
    print "FR"
    GPIO.output(11, True)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(15, False)
 
def backward_left():
    print "BL"
    GPIO.output(11, False)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(15, True)

def backward_right():
    print "BR"
    GPIO.output(11, False)
    GPIO.output(12, True)
    GPIO.output(16, False)
    GPIO.output(15, False)
   
def forward():
    print "F"
    GPIO.output(11, True)
    GPIO.output(12, False)
    GPIO.output(16, True)
    GPIO.output(15, False)

def backward():
    print "B"
    GPIO.output(11, False)
    GPIO.output(12, True)
    GPIO.output(16, False)
    GPIO.output(15, True)

def left():
    print "L"
    GPIO.output(11, False)
    GPIO.output(12, True)
    GPIO.output(16, True)
    GPIO.output(15, False)

def right():
    print "R"
    GPIO.output(11, True)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(15, True)

def nutral():
    print "N"
    GPIO.output(11, False)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(15, False)
########################## Movement Definitions END ########################

GPIO.output(18, True) #Status-LED-On
def sigint_handler(signum, frame): #Catching Ctrl+c
    GPIO.output(18, False) #Status-LED-Off
    pygame.quit()
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            GPIO.output(18, False) #Status-LED-Off
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print ("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print ("Joystick button released.")
           
 
    joystick_count = pygame.joystick.get_count() #Get Joystick Count
    if joystick_count == 0:
        GPIO.output(18, False) #Status-LED-Off
     
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    #Sensor Input
    fl = GPIO.input(7)
    fc = GPIO.input(8)
    fr = GPIO.input(10)
    bl = GPIO.input(23)
    bc = GPIO.input(24)
    br = GPIO.input(26)
    #Start Writing Yout Code From Here
    if ((fc == 1 or fr == 1 or fl == 1) and (bc == 1 or br == 1 or bl == 1)):
       if (joystick.get_axis(0) < -0.5): #Left
          left()
       elif (joystick.get_axis(0) > 0.5): #Right
            right()
       else:
         nutral()
    
    else:
       if (fc == 1): #forward_sensor blocked
          if (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) < -0.5): #Backward_Left
             backward_left()
          elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) > 0.5): #Backward_Right
               backward_right()
          elif (joystick.get_axis(1) < -0.5): #Forward
               nutral()          
          elif (joystick.get_axis(1) > 0.5): #backward
               backward()
          elif (joystick.get_axis(0) < -0.5): #Left
               left()
          elif (joystick.get_axis(0) > 0.5): #Right
               right()
          else:
               nutral()
       
       elif (bc == 1):
          
          if (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) < -0.5): #Forward_Left
               forward_left()
          elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) > 0.5): #Forward_Right
               forward_right()
          elif (joystick.get_axis(1) < -0.5): #Forward
               forward()
          elif (joystick.get_axis(1) > 0.5): #backward
             nutral()
          elif (joystick.get_axis(0) < -0.5): #Left
               left()
          elif (joystick.get_axis(0) > 0.5): #Right
               right()
          else:
               nutral()

       elif (fl == 1): #forward_left sensor blocked
          if (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) < -0.5): #Forward_Left
             nutral()
          elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) > 0.5): #Forward_Right
             forward_right()
          elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) < -0.5): #Backward_Left
               backward_left()
          elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) > 0.5): #Backward_Right
               backward_right()
          elif (joystick.get_axis(1) < -0.5): #Forward
               nutral()
          elif (joystick.get_axis(1) > 0.5): #backward
               backward()
          elif (joystick.get_axis(0) < -0.5): #Left
               left()
          elif (joystick.get_axis(0) > 0.5): #Right
               right()
          else:
               nutral()

       elif (fr == 1): #forward_right sensor blocked
          if (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) > 0.5): #Forward_Right
             nutral()
          elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) < -0.5): #Forward_Left
               forward_left()
          elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) < -0.5): #Backward_Left
               backward_left()
          elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) > 0.5): #Backward_Right
               backward_right()
          elif (joystick.get_axis(1) < -0.5): #Forward
               nutral()
          elif (joystick.get_axis(1) > 0.5): #backward
               backward()
          elif (joystick.get_axis(0) < -0.5): #Left
               left()
          elif (joystick.get_axis(0) > 0.5): #Right
               right()      
          else:
               nutral()

       
   

       elif (bl == 1):
            if (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) < -0.5): #Backward_Left
               nutral()
            elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) < -0.5): #Forward_Left
                 forward_left()
            elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) > 0.5): #Forward_Right
                 forward_right()
            elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) > 0.5): #Backward_Right
                 backward_right()
            elif (joystick.get_axis(1) < -0.5): #Forward
                 forward()
            elif (joystick.get_axis(0) < -0.5): #Left
                 left()
            elif (joystick.get_axis(0) > 0.5): #Right
                 right()
            else:
                 nutral()

       elif (br == 1):
            if (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) > 0.5): #Backward_Right
               nutral()
            elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) < -0.5): #Forward_Left
                 forward_left()
            elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) > 0.5): #Forward_Right
                 forward_right()
            elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) < -0.5): #Backward_Left
                 backward_left()
            elif (joystick.get_axis(1) < -0.5): #Forward
                 forward()
            elif (joystick.get_axis(0) < -0.5): #Left
                 left()
            elif (joystick.get_axis(0) > 0.5): #Right
                 right()
            else:
                 nutral()

       else: # All sensors free and also the controll flow for movement
           if (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) < -0.5): #Forward_Left
              forward_left()
           elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(0) > 0.5): #Forward_Right
                forward_right()
           elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) < -0.5): #Backward_Left
                backward_left()
           elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(0) > 0.5): #Backward_Right
                backward_right()
           elif (joystick.get_axis(1) < -0.5): #Forward
                forward()
           elif (joystick.get_axis(1) > 0.5): #backward
                backward()
           elif (joystick.get_axis(0) < -0.5): #Left
                left()
           elif (joystick.get_axis(0) > 0.5): #Right
                right()
           else:
                nutral()



    time.sleep(0.01)  #refresh rate 
    # ALL CODE SHOULD GO ABOVE THIS COMMENT
    
# Use Ctrl+C to quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.

pygame.quit ()
