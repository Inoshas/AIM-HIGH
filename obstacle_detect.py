
import os
os.system('cls' if os.name == 'nt' else 'clear')

import time
from buildhat import Motor, MotorPair, ColorSensor, DistanceSensor
import datetime
from datetime import datetime

#Define motor pair:
pair = MotorPair('A', 'B')
color =ColorSensor('C')
dist=DistanceSensor('D', threshold_distance=100)

# Target value to stay in the black-white line : Left =black, right=white
target_light=52

# Tunned values for kp,ki,kd
kp=1.5
ki=0.005
kd=0.01

# Initializing the values
previous_error=0
accum_error=0

# When define D value we need this to avoid division by zero
# or very low value
time_difference1=.0001
time_difference2=1000
#current_time=0

pair.set_default_speed(15)

current_time=datetime.now()

def path_follow():
    global previous_error, accum_error, time_difference1,time_difference2, current_time
	# Propotional(P)
    current_error=color.get_reflected_light() - target_light
	# Differential (D)
    error_difference=current_error-previous_error
    # Integral (I)
    accum_error = accum_error+ current_error

    print(current_error , " ce " , error_difference , "ed" , accum_error , "ae" )
    	
	#With PID
	
	# tunning can be start  just setting ki=0 , and kd=0 
    pair.start(current_error*kp+ (accum_error*ki*time_difference1)+ (error_difference*kd/time_difference2)) 
    
    	# Reassign values for next round
    previous_error = current_error
    previous_time = current_time
	
    current_time = datetime.now()
    time_difference1= (current_time-previous_time).total_seconds()
    time_difference2= time_difference1
 
    	#Printing test values ::::
    print("ref_differ =" , current_error)
    print( "  error _differ_proptional =", error_difference*kp)
    print( "accum_errro_integration" , accum_error*ki*time_difference1 )
    print("error_differential", error_difference/time_difference2*kd)
    print("time_difference", time_difference1)

def distance_cal():
	global distance
	distance=dist.get_distance()
	if distance > 150 or distance ==-1:
		path_follow()
	else: 
		pair.stop()

	

while True:
	distance_cal()
	print("distance:", distance)
	
