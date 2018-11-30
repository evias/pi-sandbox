#!/usr/bin/python3

# This script is used to test a simple raspberry pi breadboard prototyping
# scheme presented as follows:
# - GPIO PIN #18 coupled to a press button (shutdown button)
#
# LED groups are numbered from 1 to 8, the first LED group is
# on the right side when facing the breadboard with lights on top.
#
# - GPIO PIN #17 coupled to a LED positive leg (LED group 1)
# - GPIO PIN #27 coupled to a LED positive leg (LED group 2)
# - GPIO PIN #22 coupled to a LED positive leg (LED group 3)
# - GPIO PIN #13 coupled to a LED positive leg (LED group 4)
# - GPIO PIN #19 coupled to a LED positive leg (LED group 5)
# - GPIO PIN #26 coupled to a LED positive leg (LED group 6)
# - GPIO PIN #20 coupled to a LED positive leg (LED group 7)
# - GPIO PIN #21 coupled to a LED positive leg (LED group 8)
#
# The LEDs are coupled to GND using a resistance of 10 Ohms. (small leds)
# The resistance must be coupled to a GND GPIO PIN. And the LEDS are coupled
# to GND using the negative leg.

import sys
import RPi.GPIO as gpio
from random import randint
import time
import datetime

at = 7
day = -1
def date_lights(pins):
    global at
    global day
    current_date = datetime.datetime.fromtimestamp(time.time())
    day = str(current_date)[8:10]
    binDay = bin(int(day))[2:]
    at = 7
    print("Illuminating: %s" % binDay.rjust(8, '0'))
    light_idx = []
    for b in binDay.rjust(8, '0'):
        if b == '1':
            light_idx.append(at)
        at = at - 1
    light_leds(pins, light_idx)

def light_leds(pins, indexes):
    print("Indexes: %s" % indexes)
    for idx in indexes:
        led = pins[idx]
        gpio.output(led, 1)

def shutdown_lights(pins):
    for led in pins:
        gpio.output(led, 0)

def watch_date_change(pins):
    global day
    current_date = datetime.datetime.fromtimestamp(time.time())
    current_day = str(current_date)[8:10]
    if current_day != day:
        print("Date changed!")
        shutdown_lights(pins)
        date_lights(pins)

gpio.setmode(gpio.BCM)

# set GPIO PIN numbers
closeButton = 18
ledRow1 = 17
ledRow2 = 27
ledRow3 = 22
ledRow4 = 13
ledRow5 = 19
ledRow6 = 26
ledRow7 = 20
ledRow8 = 21

print("Setting up device..")

# configure button input
gpio.setup(closeButton, gpio.IN, pull_up_down=gpio.PUD_UP)

# configure output to the LEDs
gpio.setup(ledRow1, gpio.OUT)
gpio.setup(ledRow2, gpio.OUT)
gpio.setup(ledRow3, gpio.OUT)
gpio.setup(ledRow4, gpio.OUT)
gpio.setup(ledRow5, gpio.OUT)
gpio.setup(ledRow6, gpio.OUT)
gpio.setup(ledRow7, gpio.OUT)
gpio.setup(ledRow8, gpio.OUT)

print("Starting action loop..")

count = 0
try:
    # action loop - this will only break if the shutdown button is pressed
    light_pins = [ledRow1, ledRow2, ledRow3, ledRow4, ledRow5, ledRow6, ledRow7, ledRow8]
    while True:
        closeInput = gpio.input(closeButton)

        if closeInput == False:
            print("Shutdown button pressed")
            break

        if count == 0:
            print("Illuminating christmas..")
            date_lights(light_pins);
        elif count > 0:
            watch_date_change(light_pins)

        if count % 500000 == 0:
            print("Watching date changes..")
            count = 1

        count += 1

    shutdown_lights([ledRow1])
    print("Goodbye.")
except KeyboardInterrupt:
    print("See you soon..")
    gpio.cleanup()
except:
    e = sys.exc_info()[0]
    print("An error happened: %s" % e)
finally:
    gpio.cleanup()


