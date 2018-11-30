#!/usr/bin/python3

# This script is used to test a simple raspberry pi breadboard prototyping
# scheme presented as follows:
# - GPIO PIN #17 coupled to a press button (LEDs button)
# - GPIO PIN #21 coupled to a press button (shutdown button)
# - GPIO PIN #19 coupled to a red LED
# - GPIO PIN #26 coupled to a green LED
# The LED are coupled to GND using a resistance of 10 Ohms. (small leds)
# The resistance must be coupled to a GND GPIO PIN. And the LEDS are coupled
# to GND using the other leg.

import sys
import RPi.GPIO as gpio
from random import randint
import time
import datetime

def date_lights(pins):
    date = date.fromtimestamp(time.time())
    day = bin(date.day)[2:]
    at = 7
    for b in day.rjust(8, '0'):
        if b == '1':
            light_led(pins, at)
        at--

def light_led(pins, binaryIndex):
    led = pins[binaryIndex];
    gpio.output(led, 1);
    time.sleep(0.5)
    gpio.output(led, 0);
    time.sleep(0.5)

def shutdown_lights(pins):
    for led in pins:
        gpio.output(led, 0)

gpio.setmode(gpio.BCM)

# make script "dynamic"
closeButton = int(input('To which GPIO PIN is the Shutdown Button attached: '))
ledRow1 = int(input('To which GPIO PIN is the first row attached: '))
ledRow2 = ledRow1 + 3
ledRow3 = ledRow2 + 3
ledRow4 = ledRow3 + 3
ledRow5 = ledRow4 + 3
ledRow6 = ledRow5 + 3
ledRow7 = ledRow6 + 3

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

# action loop - this will only break if the shutdown button is pressed
light_pins = [leftRow1, ledRow2, ledRow3, ledRow4, ledRow5, ledRow6, ledRow7]
while True:
    closeInput = gpio.input(closeButton)

    if closeInput == False:
        break

    date_lights(light_pins);

shutdown_lights(light_pins)
gpio.cleanup()
print("Hasta luego!");

