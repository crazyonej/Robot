#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os  # added so we can shut down OK
import time  # import time module
import sys
import pygame
import subprocess

# import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
# DC = 23
# SPI_PORT = 0
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position

# Load default font.
font = ImageFont.load_default()

# Service Loc
# sudo nano /lib/systemd/system/robot.service

en1 = 9
en2 = 10

BtTrue = "None"
Mode = "Manual"

# Left
M1a = 4
M1b = 17
M2a = 27
M2b = 22

Led1 = 7
Led2 = 8

# Right
LedBD0 = 18
LedBD1 = 25

BtnBlue = 23
BtnRed = 24

sensor1LED = 20
Fire = 21


AutoMode = 26
KillSwitch = 19
Killing = False

DepthTrig = 5
DepthEcho = 6

Lspd = 0
Rspd = 0

sys.stdout = sys.stderr

mac = "85:55:A2:70:33:B3"

# Settings for the joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 2                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
buttonResetEpo = 3                      # Joystick button number to perform an EPO reset (Start)
slowFactor = 0.5                        # Speed to slow to when the drive slowly button is held, e.g. 0.5 would be half speed
buttonFastTurn = 9                      # Joystick button number for turning fast (R2)
interval = 0.00                         # Time between updates in seconds, smaller responds faster but uses more processor time
# speed = 50

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1a, GPIO.OUT)
GPIO.setup(M1b, GPIO.OUT)
GPIO.setup(M2a, GPIO.OUT)
GPIO.setup(M2b, GPIO.OUT)

GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)

GPIO.setup(Led1, GPIO.OUT)
GPIO.setup(Led2, GPIO.OUT)
GPIO.setup(LedBD0, GPIO.OUT)
GPIO.setup(LedBD1, GPIO.OUT)

GPIO.setup(BtnBlue, GPIO.IN)
GPIO.setup(BtnRed, GPIO.IN)
GPIO.setup(BtnBlue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BtnRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sleeptime = 0.1
AutoModeNew = False

GPIO.setup(sensor1LED, GPIO.OUT)

GPIO.setup(Fire, GPIO.OUT)

GPIO.setup(DepthTrig, GPIO.OUT)
GPIO.setup(DepthEcho, GPIO.IN)
# GPIO.setup(AutoMode, GPIO.IN)
GPIO.setup(AutoMode, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KillSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

p1 = GPIO.PWM(en1, 1000)
p2 = GPIO.PWM(en2, 1000)
p1.start(50)
p2.start(50)

print("Starting: {}" .format(sys.argv[0]))
GPIO.output(M1a, False)
GPIO.output(M1b, False)
GPIO.output(M2a, False)
GPIO.output(M2b, False)

pygame.joystick.init()


def DisplayUpdate(Status):
    global BtTrue
    global Mode

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((x, top), "File: " + str(sys.argv[0]), font=font, fill=255)
    draw.text((x, top + 8), "Stat: " + Status, font=font, fill=255)
    draw.text((x, top + 16), "BluTooth: " + str(BtTrue), font=font, fill=255)
    draw.text((x, top + 25), "Mode: " + str(Mode), font=font, fill=255)

# print("top {}" .format(top))


disp.image(image)
disp.display()

for x in range(1, 5):
    print("Booting {1}:{0}" .format(x, sys.argv[0]))
    DisplayUpdate("Booting")
    GPIO.output(Led1, False)
    GPIO.output(Led2, False)
    time.sleep(.5)
    GPIO.output(Led1, True)
    GPIO.output(Led2, True)
    time.sleep(1)


def FireIt():
    GPIO.output(Fire, True)
    DisplayUpdate("Fired")
    time.sleep(1.5)
    GPIO.output(Fire, False)


def init():
    # gpio.setmode(gpio.BCM)
    GPIO.setup(M1a, GPIO.OUT)
    GPIO.setup(M1b, GPIO.OUT)
    GPIO.setup(M2a, GPIO.OUT)
    GPIO.setup(M2b, GPIO.OUT)


def MoveForward(tf):
    print("forward")
    # DisplayUpdate("forward")
    GPIO.output(M1a, True)
    GPIO.output(M1b, False)
    GPIO.output(M2a, True)
    GPIO.output(M2b, False)


def MoveBack(tf):
    print("back")
    # DisplayUpdate("back")
    GPIO.output(M1a, False)
    GPIO.output(M1b, True)
    GPIO.output(M2a, False)
    GPIO.output(M2b, True)


def MoveLeft(tf):
    print("left")
    # DisplayUpdate("left")
    GPIO.output(M1a, True)
    GPIO.output(M1b, False)
    GPIO.output(M2a, False)
    GPIO.output(M2b, True)


def MoveRight(tf):
    print("right")
    # DisplayUpdate("right")
    GPIO.output(M1a, False)
    GPIO.output(M1b, True)
    GPIO.output(M2a, True)
    GPIO.output(M2b, False)


def MoveCam():
    print("Moving")


def stop():
    if(M1a is True) or (M1b is True) or (M2a is True) or (M2b is True):
        print("Stop")
        # DisplayUpdate("Stop")
        GPIO.output(M1a, False)
        GPIO.output(M1b, False)
        GPIO.output(M2a, False)
        GPIO.output(M2b, False)


def Wall():
    GPIO.output(sensor1LED, True)
    time.sleep(1.0)
    GPIO.output(sensor1LED, False)


def BDConnect():
    print("BluTooth Connected")
    # subprocess.Popen(["bash", "cam.sh"])
    GPIO.output(LedBD1, True)
    GPIO.output(LedBD0, False)


def BDDisConnect():
    print("BluTooth DisConnected")
    # subprocess.Popen(["bash", "cam.sh"])
    GPIO.output(LedBD0, True)
    GPIO.output(LedBD1, False)


def SySQuit():
    print("System Quit\n")
    GPIO.output(Led1, False)
    GPIO.output(Led2, False)
    stop()
    disp.clear()
    # BDDisConnect()
    GPIO.cleanup()
    print('Print Exit\n')


def BDConnectNew():
    pygame.joystick.init()

    # Attempt to setup the joystick
    if pygame.joystick.get_count() < 1:
        # No joystick attached, toggle the LED
        print("No JoyStick")
        # BtTrue = "None"
        BDDisConnect()
        pygame.joystick.quit()
        time.sleep(0.1)
    else:
        # We have a joystick, attempt to initialise it!
        joystick = pygame.joystick.Joystick(0)
        # BDConnect()
        print('Joystick found')
        # BtTrue = "Good"
        # BDConnect()
        joystick.init()

    time.sleep(1.0)


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

    # print ("Distance:",space,"cm")

    check_front(space)
    # return distance


def check_front(dist):
    # stop()
    # print ("CheckDistance:",dist)

    if int(dist) < 25:
        print('Too close,', dist)
        stop()
        Wall()
        MoveBack(0.5)

        if int(dist) < 25:
            print('Too close,', dist)
            # stop()
            MoveLeft(0.5)
            # stop()
            # MoveBack(2)
            if dist < 25:
                print('Too close, giving up', dist)
                stop()
                # sys.exit()


def sRange(val):
    # print("sRange-",val)
    OldRange = (100 - 0)

    if (val < 50):
        NewValue = 50
    else:
        NewRange = (100 - 50)
        NewValue = (((val - 0) * NewRange) / OldRange) + 50

    spd = round(NewValue, 0)
    print("DutyCycle ", spd)
    print("TurnL ", spd - Lspd)
    print("TurnR ", spd - Rspd)
    
    p1.ChangeDutyCycle(spd - Lspd)
    p2.ChangeDutyCycle(spd - Rspd)
    # return NewValue


def sSpeed(Nspd):
    # print("sRange-",val)
    if (Nspd < 50):
        Spec = round((((Nspd - 0) * 100) / 100) + 50, 0)
        print("Spec ", Spec)
    else:
        Spec = 0

    # abs(Spec)
    return abs(Spec)


# Setup pygame and wait for the joystick to become available
os.environ["SDL_VIDEODRIVER"] = "dummy"  # Removes the need to have a GUI window
pygame.init()
# pygame.display.set_mode((1,1))
print('Waiting for joystick... (press CTRL+C to abort)')
# bluetoothctl("connect",mac)


def VidStart():
    print("StartVideo:\n")
    print("rtsp://192.168.1.222:8554/\n")
    subprocess.Popen(["bash", "strm.sh"])
    time.sleep(3)


def BluConnect():
    if pygame.joystick.get_count() < 1:
        print("Connect2Blue")
        subprocess.Popen(["bash", "blueOn.sh"])
        time.sleep(3)
    else:
        print("BluTooth Connected")
        time.sleep(3)


while True:
    try:
        try:
            pygame.joystick.init()
            BluConnect()
            # Attempt to setup the joystick
            if pygame.joystick.get_count() < 1:
                # No joystick attached, toggle the LED
                BDDisConnect()
                pygame.joystick.quit()
                time.sleep(0.1)
            else:
                # We have a joystick, attempt to initialise it!
                joystick = pygame.joystick.Joystick(0)
                BDConnect()
                break
        except pygame.error:
            # Failed to connect to the joystick, toggle the LED
            pygame.joystick.quit()
            BDDisConnect()
            time.sleep(0.1)
    except KeyboardInterrupt:
        # CTRL+C exit, give up
        print('User aborted')
        GPIO.cleanup()
        BDDisConnect()
        sys.exit()
print('Joystick found')
BDConnect()
joystick.init()

try:
    print('Press CTRL+C to quit')
    DisplayUpdate("Booting")
    # global speed
    # speed = 50
    driveLeft = 0.0
    driveRight = 0.0
    running = True
    hadEvent = False
    upDown = 0.0
    leftRight = 0.0
    camupDown = 0.0
    camleftRight = 0.0

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
                # print("Joy Btn", pygame.get.button())
                # print(pygame.key.get_pressed())
                # print(event.dict, event.joy, event.button, 'pressed')
                hadEvent = True
            elif event.type == pygame.JOYAXISMOTION:
                # A joystick has been moved
                hadEvent = True
            elif event.type == pygame.JOYHATMOTION:
                # A Hat has been moved
                print("Hat Event")
                hadEvent = True
            else:
                hadEvent = False
                stop()
                # print("Stop Event")

            if hadEvent:
                # Read axis positions (-1 to +1)
                upDown = joystick.get_axis(1)
                # leftRight = joystick.get_axis(0)
                leftRight = joystick.get_axis(2)

                # Apply steering speeds
                if not joystick.get_button(buttonFastTurn):
                    leftRight *= 0.5

                # Determine the drive power levels
                if upDown < -0.20:
                    # speed = round(-joystick.get_axis(1))
                    sRange(abs(-joystick.get_axis(1)) * 100)
                    # print("spd", abs(-joystick.get_axis(1)) *100)
                    # print("speed-", speed)
                    MoveForward(0)
                elif upDown > 0.20:
                    sRange(abs(-joystick.get_axis(1)) * 100)
                    # speed = round(-joystick.get_axis(1))
                    # print("speed-", speed)
                    MoveBack(0)
                if leftRight < -0.30:
                    # Turning left
                    # sRange(abs(-joystick.get_axis(0)) * 100)
                    Lspd = sSpeed(abs(-joystick.get_axis(0)) * 100)
                    # MoveLeft(0)
                elif leftRight > 0.30:
                    # Turning right
                    # sRange(abs(-joystick.get_axis(0)) * 100)
                    Rspd = sSpeed(abs(-joystick.get_axis(0)) * 100)
                    # MoveRight(0)
                # Check for button presses

                if joystick.get_axis(1) == 0 and joystick.get_axis(0) == 0:
                    # print("Stop Movement")
                    stop()

                # if joystick.get_axis(2) == 0 and joystick.get_axis(3) == 0:
                #    MoveCam()

                if joystick.get_button(0):
                    print("Button00 A")
                    stop()
                elif joystick.get_button(1):
                    print("Button01 B")
                    FireIt()
                elif joystick.get_button(2):
                    print("Button02 ")
                elif joystick.get_button(3):
                    print("Button03 X")
                    stop()
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
                    stop()
                elif joystick.get_button(9):
                    print("Button09 R2")
                    stop()
                elif joystick.get_button(10):
                    print("Button10 Select")
                elif joystick.get_button(11):
                    print("Button11 Start")
                    SySQuit()
                elif joystick.get_button(13):
                    print("Button13 JoyL")
                elif joystick.get_button(14):
                    print("Button14 JoyR")

        if (GPIO.input(BtnBlue) is False):
            print("Btn Blue Connect BluTooth")
            BluConnect()
        if (GPIO.input(BtnRed) is False):
            print("Btn Red Start Vid")
            VidStart()

        # Change the LED to reflect the status of the EPO latch
        if (GPIO.input(KillSwitch) is False):
            if(Killing is True):
                print("KillSwitch-", Killing)
                Killing = False
                # subprocess.Popen(["bash", "cam.sh"])
                time.sleep(1.0)
            else:
                print("KillStop-", Killing)
                Killing = True
                time.sleep(1.0)
        # Wait for the interval period
        time.sleep(interval)
    # Disable all drives
    # Print("Stop")
except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    print('Print Exit\n')
    SySQuit()
    # GPIO.cleanup()
