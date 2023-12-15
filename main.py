import os
# Clear screen ::: 
os.system('cls' if os.name == 'nt' else 'clear')
from phase1 import correct_path_follower
from phase2 import db_Qr, process_QR
from buildhat import MotorPair, ColorSensor, DistanceSensor
from datetime import datetime


picam = Picamera2()
picam.preview_configuration.main.size=(1280,720)
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()

phase2_obj=process_QR()
phase2_obj.read_QR()

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

### Initializing values for DB creation
db_name="mydatabase.db"
table_name='inventory'
qr_folder = "QR_Codes" 

name="Olive"
barcode="OL-finnishbrand-005"
rackdetails="H67-R9-C1" 
quantity=9


#### main loop:::.
#### create main object for phase1:
main_cpf = correct_path_follower(pair, color,dist, previous_error, accum_error,time_difference1, time_difference2, target_light,fixed_speed,current_time, kp, kd, ki, phase2_obj)



## Create_object for phase 2
main_dbqr=db_Qr(db_name, table_name,  name, barcode, rackdetails, quantity, qr_folder )
main_pqr=process_QR()

################################################################
### Uncomment this if you want to add data to dB and generate QR:::
# Add another row to db and create QR code:
#main_dbqr.db_table()
#main_dbqr.generate_QR()

#######################################################33

while True:
    main_cpf.distance_cal()

	



