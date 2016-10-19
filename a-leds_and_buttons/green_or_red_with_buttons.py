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

def light_led(ledPin, delay):
    gpio.output(ledPin, 1)
    time.sleep(delay)
    gpio.output(ledPin, 0)
    time.sleep(delay)

gpio.setmode(gpio.BCM)

# make script "dynamic"
closeButton = int(input('Which GPIO PIN is the Shutdown Button on: '))
lightButton = int(input('Which GPIO PIN is the LEDs Button on: '))
ledRed   = int(input('Which GPIO PIN are the RED LEDs on: '))
ledGreen = int(input('Which GPIO PIN are the GREEN LEDs on: '))

# configure button input
gpio.setup(lightButton, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(closeButton, gpio.IN, pull_up_down=gpio.PUD_UP)

# configure output to the LEDs
gpio.setup(ledRed, gpio.OUT)
gpio.setup(ledGreen, gpio.OUT)

# while the script is running, the green LED will be ON
gpio.output(ledGreen, 1)

# action loop - this will only break if the shutdown button is pressed
while True:
    lightInput = gpio.input(lightButton)
    closeInput = gpio.input(closeButton)

    if closeInput == False:
        break

    if lightInput == False:
        light_led(ledRed, 0.2)

gpio.output(ledGreen, 0)
gpio.cleanup()
print("Tschüss")

