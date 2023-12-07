import os
# Clear screen ::: 
os.system('cls' if os.name == 'nt' else 'clear')


import time
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

class correct_path_follower():
    def __init__(self, pair, color,dist, previous_error, accum_error,time_difference1, time_difference2, target_light,fixed_speed,current_time, kp, kd, ki):
     
        self.pair=pair
        self.color=color
        self.dist=dist
        self.previous_error=previous_error
        self.accum_error=accum_error
        self.time_difference1=time_difference1
        self.time_difference2=time_difference2
        self.current_time=current_time
        self.target_light=target_light
        self.fixed_speed=fixed_speed
        self.current_time=current_time
        self.kp=kp  
        self.ki=ki
        self.kd=kd
        
    
    ### The  path following function:::
    def path_follow(self):  
		#global previous_error, accum_error, time_difference1,time_difference2, current_time
		# Propotional(P)	
        current_error=self.color.get_reflected_light() - self.target_light
		# Differential (D)
        error_difference=current_error-self.previous_error
			# Integral (I)
        self.accum_error = self.accum_error + current_error
		#print(current_error , " ce " , error_difference , "ed" , accum_error , "ae" )
			
		#With PID correction : 
        new_speed=current_error*self.kp +(self.accum_error*self.ki*self.time_difference1)+(error_difference*self.kd/self.time_difference2)
        print("new_speed",new_speed, "**", error_difference*self.kd)
		# adjust speed:::
        self.pair.start(-abs(self.fixed_speed-new_speed), abs(self.fixed_speed  + new_speed)) 
		
        # Reassign values for next round
        self.previous_error = current_error
        self.previous_time= current_time
        self.current_time = datetime.now()
        self.time_difference1= (self.current_time-self.previous_time).total_seconds()
        self.time_difference2= time_difference1
             
       
        return self.previous_error, self.previous_time, self.current_time,self.time_difference1, self.time_difference2
	    

    
	## Act based on current Distance:::
    def distance_cal(self):
        #global distance
        global previous_error, previous_time, current_time ,time_difference1, time_difference2
        
        distance=self.dist.get_distance()
        if distance > 150 or distance ==-1:
            previous_error, previous_time, current_time ,time_difference1, time_difference2=main_cpf.path_follow()
            
        else:

            previous_error, current_time ,time_difference1, time_difference2=main_cpf.obstacle_avoid()
                
    #### Turning different directions
    def turn_right(self):
        self.pair.run_for_degrees(225,-20,-20)
        self.pair.stop()
        time.sleep(.5)

    def turn_left(self):
        self.pair.run_for_degrees(225,20,20)
        self.pair.stop()
        time.sleep(.5)
        
    #### Moving  front  :

    def move_forward(self):
        self.pair.run_for_rotations(2,-60,60)
        self.pair.stop()
        time.sleep(.5)

    ### Avoid obstacle  in right side::
    def right_avoid(self):
        print("I select first path: turn right")
        main_cpf.move_forward()
        main_cpf.turn_left()
        main_cpf.move_forward()
        main_cpf.turn_left()
        main_cpf.move_forward()
        main_cpf.turn_right()


    # Avoid obstacle in left side::
    def left_avoid(self):
        #global distance
        print("I select turn left")
        main_cpf.turn_left()
        main_cpf.turn_left()
        time.sleep(1)	
        distance=self.dist.get_distance()
        if distance < 300 and distance !=-1:
            main_cpf.turn_right()
            self.pair.stop()
            time.sleep(3)
            self.pair.start(40,-40)
                        
        else:
            main_cpf.move_forward()
            main_cpf.turn_right()
            main_cpf.move_forward()		
            main_cpf.turn_right()
            main_cpf.move_forward()
            main_cpf.turn_left()

    def obstacle_avoid(self):

        self.previous_error=0
        self.accum_error=0
        # Reset values:::
        self.time_difference1=.0001
        self.time_difference2=1000


        print("--------------Obstacle avoiding started------")
        main_cpf.turn_right()
        time.sleep(1)
        distance=self.dist.get_distance()
        print("dis", distance)
        print("Here we check direction to turn")
        if distance < 300 and distance != -1:
            main_cpf.left_avoid()
        else:
            main_cpf.right_avoid()
        self.current_time=datetime.now()
        
        print("--------------Obstacle avoiding stoped------")
        
        return self.previous_error, self.current_time , self.time_difference1, self.time_difference2





#### main loop:::.
#### create main object
main_cpf = correct_path_follower(pair, color,dist, previous_error, accum_error,time_difference1, time_difference2, target_light,fixed_speed,current_time, kp, kd, ki)

while True:
    main_cpf.distance_cal()
   
	



