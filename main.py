import os
# Clear screen ::: 
os.system('cls' if os.name == 'nt' else 'clear')

import time
from buildhat import Motor, MotorPair, ColorSensor, DistanceSensor
import datetime
from datetime import datetime

#Define motor pair and sensors
pair = MotorPair('A', 'B')
color =ColorSensor('C')
dist=DistanceSensor('D', threshold_distance=100)

# Target value to stay in the black-white line : Left =black, right=white
target_light=52

# PID controller tunned values for kp,ki,kd
kp=.27
ki=0.003
kd=0.03

## Set this to slowdown the motors with PID error
fixed_speed=25


# Initializing the values
previous_error=0
accum_error=0

# When define D value we need this to avoid division by zero
# or very low value
time_difference1=.0001
time_difference2=1000

###  Mindstorm motors usually not working properly for less
##thank 25 speed: In order to work properly we need to  change bias values:

pair._leftmotor.plimit(1.0)
pair._leftmotor.bias(0.5)
pair._rightmotor.plimit(1.0)
pair._rightmotor.bias(0.5)

# Define default speed to begin
pair.set_default_speed(15)

# get current time:
current_time=datetime.now()


### The  path following function:::
def path_follow():
	global previous_error, accum_error, time_difference1,time_difference2, current_time
	# Propotional(P)	
	current_error=color.get_reflected_light() - target_light
	# Differential (D)
	error_difference=current_error-previous_error
    	# Integral (I)
	accum_error = accum_error + current_error
	#print(current_error , " ce " , error_difference , "ed" , accum_error , "ae" )
    	
	#With PID correction : 
	new_speed=current_error*kp +(accum_error*ki*time_difference1)+ (error_difference*kd/time_difference2)
	# adjust speed:::
	pair.start(-abs(fixed_speed-new_speed), abs(fixed_speed  + new_speed)) 
    
    	# Reassign values for next round
	previous_error = current_error
	previous_time = current_time
	current_time = datetime.now()
	time_difference1= (current_time-previous_time).total_seconds()
	time_difference2= time_difference1
''' 
    	#Printing test values ::::
	print("ref_differ =" , current_error)
	print("left_speed:  ", pair._leftmotor.get_speed(), "right speed: ", pair._rightmotor.get_speed())
	print( "  error _differ_proptional =", error_difference*kp)
	print( "accum_errro_integration" , accum_error*ki*time_difference1 )
	print("error_differential", error_difference/time_difference2*kd)
	#print("time_difference", time_difference1)
'''

## Act based on current Distance:::
def distance_cal():
	global distance
	
	distance=dist.get_distance()
	if distance > 150 or distance ==-1:
		path_follow()
	else:
		obstacle_avoid()
		
#### Turning different directions
def turn_right():
	pair.run_for_degrees(225,-20,-20)
	pair.stop()
	time.sleep(.5)

def turn_left():
	pair.run_for_degrees(225,20,20)
	pair.stop()
	time.sleep(.5)
#### Moving  front directions :

def move_forward():
	pair.run_for_rotations(2,-60,60)
	pair.stop()
	time.sleep(.5)

### Avoid obstacle  in right side::
def right_avoid():
	print("I select first path: turn right")
	move_forward()
	turn_left()
	move_forward()
	turn_left()
	move_forward()
	turn_right()
 
 
# Avoid obstacle in left side::
def left_avoid():
	global distance
	print("I select turn left")
	turn_left()
	turn_left()
	time.sleep(1)	
	distance=dist.get_distance()
	if distance < 300 and distance !=-1:
		turn_right()
		pair.stop()
		time.sleep(3)
		pair.start(40,-40)
			
	else:
		move_forward()
		turn_right()
		move_forward()		
		turn_right()
		move_forward()
		turn_left()

def obstacle_avoid():
	global previous_error, accum_error, time_difference1,time_difference2, current_time
	global distance
	previous_error=0
	accum_error=0
	# Reset values:::
	time_difference1=.0001
	time_difference2=1000


	print("--------------Obstacle avoiding started------")
	turn_right()
	time.sleep(1)
	distance=dist.get_distance()
	print("dis", distance)
	print("Here we check direction to turn")
	if distance < 300 and distance != -1:
		left_avoid()
	else:
		right_avoid()
	current_time=datetime.now()
	
	print("--------------Obstacle avoiding stoped------")
#### main loop:::.


while True:
	distance_cal()
	print("distance:", distance)
	
