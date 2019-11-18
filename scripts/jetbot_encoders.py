#!/usr/bin/env python
import rospy
import time
import Jetson.GPIO as GPIO

from std_msgs.msg import Int32


encoderLeftCount = 0
encoderRightCount = 0

def initGPIO():
	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(31, GPIO.IN)
	GPIO.setup(33, GPIO.IN)
	GPIO.setup(35, GPIO.IN)
	GPIO.setup(37, GPIO.IN)
	GPIO.remove_event_detect(31)
	GPIO.remove_event_detect(33)
	GPIO.remove_event_detect(35)
	GPIO.remove_event_detect(37)
	# add edge detection
	GPIO.add_event_detect(31, GPIO.BOTH, callback=callback31)
	GPIO.add_event_detect(33, GPIO.BOTH, callback=callback33)
	GPIO.add_event_detect(35, GPIO.BOTH, callback=callback35)
	GPIO.add_event_detect(37, GPIO.BOTH, callback=callback37)

# define callback functions
def callback31(channel):
	global encoderLeftCount
	if GPIO.input(33) == GPIO.HIGH:
		if GPIO.input(31) == GPIO.HIGH:
			encoderLeftCount+=1
		else:
			encoderLeftCount-=1
	else:
		if GPIO.input(31) == GPIO.HIGH:
			encoderLeftCount-=1
		else:
			encoderLeftCount+=1

def callback33(channel):
	global encoderLeftCount
	if GPIO.input(31) == GPIO.HIGH:
		if GPIO.input(33) == GPIO.HIGH:
			encoderLeftCount-=1
		else:
			encoderLeftCount+=1
	else:
		if GPIO.input(33) == GPIO.HIGH:
			encoderLeftCount+=1
		else:
			encoderLeftCount-=1

# define callback functions
def callback35(channel):
	global encoderRightCount
	if GPIO.input(37) == GPIO.HIGH:
		if GPIO.input(35) == GPIO.HIGH:
			encoderRightCount+=1
		else:
			encoderRightCount-=1
	else:
		if GPIO.input(35) == GPIO.HIGH:
			encoderRightCount-=1
		else:
			encoderRightCount+=1

def callback37(channel):
	global encoderRightCount
	if GPIO.input(35) == GPIO.HIGH:
		if GPIO.input(37) == GPIO.HIGH:
			encoderRightCount-=1
		else:
			encoderRightCount+=1
	else:
		if GPIO.input(37) == GPIO.HIGH:
			encoderRightCount+=1
		else:
			encoderRightCount-=1


# initialization
if __name__ == '__main__':
	encoderRightCount = 0
	encoderLeftCount = 0
	# setup GPIO
	initGPIO()

	# setup ros node
	rospy.init_node('jetbot_encoders')

	#rospy.Subscriber('~cmd_vel', Twist, on_cmd_vel)	
	pubL = rospy.Publisher('encoder_left_wheel', Int32, queue_size=10)
	pubR = rospy.Publisher('encoder_right_wheel', Int32, queue_size=10)

	r = rospy.Rate(50)
	while not rospy.is_shutdown():
		pubL.publish(encoderLeftCount)
		pubR.publish(encoderRightCount)
		r.sleep()

	# stop motors before exiting
	GPIO.cleanup()
	GPIO.remove_event_detect(31)
	GPIO.remove_event_detect(33)
	GPIO.remove_event_detect(35)
	GPIO.remove_event_detect(37)

