import time
import RPi.GPIO as gpio
import SimpleCV
import piModules
import motors

# Returns True if the circle is in range of the center of the cameras view
def circleInRange(offset):
	if offset >= -7 and offset <= 7: # 7 inch range on either side before rotation is triggered
		return True
	else:
		return False

# Returns true if the circle has been found while turning (which means the robot should stop)
def circleFound(offset, turningRight, turningLeft):
	if turningRight and offset > 0 and offset < 14:
		return True
	elif turningLeft and offset < 0 and offset > -14:
		return True
	else:
		return False

# Rotates depending on the circles position
def rotate(circleOffset,f):
	global stagnantStartTime 
	
	inRange = circleInRange(circleOffset)

	# If the circle is out of the 7 inch range
	if not(inRange):
		# If circle is offset to the right
		if circleOffset > 0:
			turningRight = True
			turningLeft = False
			start = time.time()
			motors.pivotRight()
		# If circle is offset to the left
		elif circleOffset < 0:
			turningRight = False
			turningLeft = True
			start = time.time()
			motors.pivotLeft()

		# Robot rotates until this loop is exited
		while True:	
			currentCircleOffset = piModules.getOffset(cam)
			if circleFound(currentCircleOffset, turningRight, turningLeft):	# Circle found, stop turning, write movements to file
				end = time.time()
				if stagnantStartTime is not(None):
					f.write('S:' + str(end - stagnantStartTime) + '\n')
					stagnantStartTime = None
				if turningRight:
					f.write('R:' + str(end - start) + '\n')
				elif turningLeft:
					f.write('L:' + str(end - start) + '\n')			
				resetTurning()				
				break
	else:
		if stagnantStartTime is None:
			stagnantStartTime = time.time()	

# Stops the robot when circleFound
def resetTurning():
	turningRight = False
	turningLeft = False
	motors.stop()

# Handles forward/backward movement
def correctDistance(f):
	global stagnantStartTime

	direction = 'stopped'
	start = None

	# Loops until the robot is between MIN_RANGE and MAX_RANGE
	while True:
		distance = piModules.getDistance() # Gets distance between cardboard and robot

		if distance >= MAX_RANGE: # Forward
			direction = 'forward'
			if start is None:
				start = time.time()
			motors.forward()
		elif distance <= MIN_RANGE: # Reverse
			direction = 'reverse'
			if start is None:
				start = time.time()
			motors.reverse()
		else: # Robot is in "steady" range, write movement to file
			end = time.time()
			if direction is 'stopped':
				if stagnantStartTime is None:
					stagnantStartTime = time.time()
			elif direction is 'forward':
				if stagnantStartTime is not(None):
					f.write('S:' + str(end - stagnantStartTime) + '\n')
					stagnantStartTime = None
				f.write('F:' + str(end - start) + '\n')
			elif direction is 'reverse':
				if stagnantStartTime is not(None):
					f.write('S:' + str(end - stagnantStartTime) + '\n')
					stagnantStartTime = None
				f.write('B:' + str(end - start) + '\n')
			motors.stop()
			break
try:
	MAX_RANGE = 20 # Max distance between cardboard and robot
	MIN_RANGE = 15 # Min distance between cardboard and robot

	stagnantStartTime = None # Keeps track of pauses in the robot's movement
	
	cam = SimpleCV.Camera()
        motors.init()

	f = open('replay.txt', 'w') # Create file for the replay

	# Main Loop
	while True:
		circleOffset = None

		# Loops until the circle is found
		while circleOffset is None:
			circleOffset = piModules.getOffset(cam)

		rotate(circleOffset, f) # Rotate
		correctDistance(f) # Forward Backward
except KeyboardInterrupt:
	print("CTRL-C detected, exiting program")
finally:
	f.write('END\n') # Write END on the file
	f.close()
	print("gpio.cleanup()")
	gpio.cleanup() # Cleanup GPIO pins


