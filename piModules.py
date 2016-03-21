### All functions that need to access the pi modules (camera and distance sensor) ###

import time 
import RPi.GPIO as gpio
import SimpleCV

## Handles all concerns with the distance sensor ##
# This sensor sends out a signal and pulses high when that signal bounces back,
# this can be used to determine distance using the speed of sound constant

# GPIO pin number assignments
TRIG = 12
ECHO = 16

def getDistance():
	# Initializing pins
	gpio.setup(TRIG, gpio.OUT)
	gpio.setup(TRIG, 0)

	gpio.setup(ECHO, gpio.IN)

	time.sleep(0.1)

	# Pulse Trigger
	gpio.output(TRIG, 1)
	time.sleep(0.00001)
	gpio.output(TRIG, 0)

	# Record start time of pulse
	while gpio.input(ECHO) == 0:
		pass
	start = time.time()

	# Record time when pule was received
	while gpio.input(ECHO) == 1:
		pass
	stop = time.time()

	return (stop - start) * 17000 # Return in seconds

## Handles all concerns with the camera, mainly with SimpleCV ##

def getOffset(cam):
	img = cam.getImage().flipHorizontal() # Image needs to be flipped because my camera is upside-down

	dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2) # Get colors furthest from black (white)
	segmented = dist.stretch(50, 255) # Push all colors with value > 50 to black
	blobs = segmented.findBlobs()

	if blobs:
		circles = blobs.filter([b.isCircle(1) for b in blobs])
		if circles:
			return circles[-1].x - img.width/2 # Return the difference between the two centers
