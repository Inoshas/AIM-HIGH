import os
# Clear screen ::: 
os.system('cls' if os.name == 'nt' else 'clear')
from phase1 import correct_path_follower

from buildhat import MotorPair, ColorSensor, DistanceSensor

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
previous_time=0
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
pair.start(-15,15)
# get current time:
current_time=datetime.now()


#### main loop:::.
#### create main object
main_cpf = correct_path_follower(pair, color,dist, previous_error, accum_error,time_difference1, time_difference2, target_light,fixed_speed,current_time, kp, kd, ki)

while True:
    main_cpf.distance_cal()
   
	



