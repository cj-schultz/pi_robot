# Before Refactor

import RPi.GPIO as gpio
import time

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(7, gpio. OUT)
	gpio.setup(11, gpio.OUT)
	gpio.setup(13, gpio.OUT)
	gpio.setup(15, gpio.OUT)

def forward(tf):
	gpio.output(7, True) 
	gpio.output(11, False) 
	gpio.output(13, False) 
	gpio.output(15, True) 
	time.sleep(tf)

def reverse(tf):
	gpio.output(7, False)
	gpio.output(11, True)
	gpio.output(13, True)
	gpio.output(15, False)
	time.sleep(tf)

def pivotLeft(tf):
	gpio.output(7, True)
	gpio.output(11, False)
	gpio.output(13, True)
	gpio.output(15, False)
	time.sleep(tf)

def pivotRight(tf):
	gpio.output(7, False)
	gpio.output(11, True)
	gpio.output(13, False)
	gpio.output(15, True)
	time.sleep(tf)

def stop():
	gpio.output(7, True)
	gpio.output(11, True)
	gpio.output(13, True)
	gpio.output(15, True)
init()

try:
	init()
	with open('replay.txt') as f:
		for line in f:
				
			line = line.strip()
			if line is 'END':
				print('done')
				gpio.cleanup()
				break	

			else:
				tokens = line.split(':')
				direction = tokens[0]
				tf = float(tokens[1])	

				if direction is 'L':
					pivotLeft(tf)
					stop()
				elif direction is 'R':
					pivotRight(tf)
					stop()
				elif direction is 'F':
					forward(tf)
					stop()
				elif direction is 'B':
					reverse(tf)
					stop()		
				elif direction is 'S':
					stop()
					time.sleep(tf)
finally:
	gpio.cleanup()
