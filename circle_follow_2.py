import time
import RPi.GPIO as gpio
import SimpleCV

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(7, gpio. OUT)
	gpio.setup(11, gpio.OUT)
	gpio.setup(13, gpio.OUT)
	gpio.setup(15, gpio.OUT)

	gpio.output(7, True)
	gpio.output(11, True)
	gpio.output(13, True)
	gpio.output(15, True)

def pivotLeft():
	gpio.output(7, True)
	gpio.output(11, False)
	gpio.output(13, True)
	gpio.output(15, False)

def pivotRight():
	gpio.output(7, False)
	gpio.output(11, True)
	gpio.output(13, False)
	gpio.output(15, True)

def forward():
	gpio.output(7, True) # Right, Reverse
	gpio.output(11, False) # Right, Forward
	gpio.output(13, False) # Left, Forward
	gpio.output(15, True) # Left, Reverse

def reverse():
	gpio.output(7, False)
	gpio.output(11, True)
	gpio.output(13, True)
	gpio.output(15, False)

def stop():
	gpio.output(7, True)
	gpio.output(11, True)
	gpio.output(13, True)
	gpio.output(15, True)

def getOffset(cam):
	img = cam.getImage().flipHorizontal()
	
	dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
	segmented = dist.stretch(50, 255)
	blobs = segmented.findBlobs()

	if blobs:
		circles = blobs.filter([b.isCircle(1) for b in blobs])
		if circles:
			return circles[-1].x - img.width/2	

def circleInRange(offset):
	if offset >= -7 and offset <= 7:
		return True
	else:
		return False

def circleFound(offset, turningRight, turningLeft):
	if turningRight and offset > 0 and offset < 14:
		return True
	elif turningLeft and offset < 0 and offset > -14:
		return True
	else:
		return False

def getDistance():
	gpio.setup(TRIG, gpio.OUT)
	gpio.output(TRIG, 0)
	
	gpio.setup(ECHO, gpio.IN)
	
	time.sleep(0.1)

	gpio.output(TRIG, 1)
	time.sleep(0.00001)
	gpio.output(TRIG, 0)

	while gpio.input(ECHO) == 0:
		pass
	start = time.time()

	while gpio.input(ECHO) == 0:
		pass
	start = time.time()

	while gpio.input(ECHO) == 1:
		pass
	stop = time.time()
	
	return (stop - start) * 17000

def rotate(circleOffset):
	inRange = circleInRange(circleOffset)
	if not(inRange):
		if circleOffset > 0:
			turningRight = True
			turningLeft = False
			pivotRight()
		elif circleOffset < 0:
			turningRight = False
			turningLeft = True
			pivotLeft()
		while True:	
			currentCircleOffset = getOffset(cam)
			if circleFound(currentCircleOffset, turningRight, turningLeft):				
				resetTurning()				
				break

def resetTurning():
	turningRight = False
	turningLeft = False
	stop()

def correctDistance():
	while True:
		distance = getDistance()

		if distance >= MAX_RANGE:
			forward()
		elif distance <= MIN_RANGE:
			reverse()
		else:
			stop()
			break

MAX_RANGE = 20
MIN_RANGE = 15
TRIG = 12
ECHO = 16

cam = SimpleCV.Camera()
init()

try:
	while True:
		circleOffset = None

		while circleOffset is None:
			circleOffset = getOffset(cam)

		rotate(circleOffset)
		correctDistance()
except KeyboardInterrupt:
	print("CTRL-C detected, exiting program")
finally:
	print("gpio.cleanup()")
	gpio.cleanup()


