#!/usr/bin/env python

# servos_pot.py
# 2017-04-25
# Public Domain

import time

import pigpio  # http://abyz.me.uk/rpi/pigpio/python.html

SERVOS=[14, 15, 16, 17, 18, 19] # List of GPIO connected to servos.

MIN_SERVO=500
MAX_SERVO=2500

MIN_POT_CAP=0
MAX_POT_CAP=1023

def map(val, in_min, in_max, out_min, out_max):
  return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

pi = pigpio.pi() # Connect to Pi.

if not pi.connected:
  exit()

adc = pi.spi_open(0, 40000) # Open SPI channel 0 at 40kbps.

while True:

   try:

     for i in range(len(SERVOS)):

        # This code assumes that an 8-channel MCP3008 ADC is connected
        # to the main SPI channel 0

        c, d = pi.spi_xfer(adc, [1, (8+i)<<4, 0]) # Read channel i.

        v = ((d[1]<<8) | d[2]) & 0x3FF

        micros = map(v, MIN_POT_CAP, MAX_POT_CAP, MIN_SERVO, MAX_SERVO)

        pi.set_servo_pulsewidth(SERVOS[i], micros)

     time.sleep(0.02)

   except:

      break

print("\nexiting...")

pi.spi_close(adc) # Release SPI handle.

for s in SERVOS:
   pi.set_servo_pulsewidth(s, 0) # Switch each servo off.

pi.stop() # Disconnect from Pi.