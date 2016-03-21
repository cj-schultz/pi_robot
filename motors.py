### Motor Controller ###

# Note: setting a motor to False gives that motor power

import RPi.GPIO as gpio

RR = 7  # Right Reverse
RF = 11 # Right Forward
LF = 13 # Left Forward
LR = 15 # Left Reverse

def init():
	gpio.setmode(gpio.BOARD)
	
	gpio.setup(RR, gpio.OUT)
	gpio.setup(RF, gpio.OUT)
	gpio.setup(LF, gpio.OUT)
	gpio.setup(LR, gpio.OUT)

	gpio.output(RR, True)
	gpio.output(RF, True)
	gpio.output(LF, True)
	gpio.output(LR, True)

def forward():
	gpio.output(RR, True)
	gpio.output(RF, False)
	gpio.output(LF, False)
	gpio.output(LR, True)

def reverse():
	gpio.output(RR, False)
	gpio.output(RF, True)
	gpio.output(LF, True)
	gpio.output(LR, False)

def pivotLeft():
	gpio.output(RR, True)
	gpio.output(RF, False)
	gpio.output(LF, True)
	gpio.output(LR, False)

def pivotRight():
	gpio.output(RR, False)
	gpio.output(RF, True)
	gpio.output(LF, False)
	gpio.output(LR, True)

def stop():
	gpio.output(RR, True)
	gpio.output(RF, True)
	gpio.output(LF, True)
	gpio.output(LR, True)
