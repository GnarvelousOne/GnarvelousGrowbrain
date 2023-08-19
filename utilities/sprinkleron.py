#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Sprinklers On:

# set pump GPIO:
pump = 6

GPIO.setup(pump, GPIO.OUT)
GPIO.output(pump, False)

# outlets are numbered from right to left
    # 1 is 5 
    # 2 is 6 
    # 3 is 13
    # 4 is 19
    # 5 is 26
    # 6 is 16
    # 7 is 20
    # 8 is 21
