#!/usr/bin/python3

import random
from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)

		
while True:
	lightint = random.randint(1,5)
	print(lightint)
	GPIO.output(5, False)
	sleep(lightint*.1)
	lightint = random.randint(1,5)
	print(lightint)
	GPIO.output(5, True)
	sleep(lightint*.1)	
