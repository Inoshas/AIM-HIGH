
import time
from buildhat import Motor, MotorPair

#Define motor pair:
pair = MotorPair('A', 'B')
'''
pair._leftmotor.plimit(1.0)
pair._leftmotor.bias(0.4)
pair._rightmotor.plimit(1.0)
pair._rightmotor.bias(0.4)
'''

def handle_motor(speed, pos, apos):
    """Motor data

    :param speed: Speed of motor
    :param pos: Position of motor
    :param apos: Absolute position of motor
    """
    print("Motor", speed, pos, apos)

'''
#set motors  default values:::
# Better define this if you use run_for_seconds:::

pair._leftmotor.set_default_speed(-60)
pair._rightmotor.set_default_speed(60)
'''

##Print left and right motor values
print("This print motor speed")
pair._leftmotor.when_rotated = handle_motor
pair._rightmotor.when_rotated =handle_motor

pair.start()
print("Forward moving start here----")
#Run forward for 3 rotations::
pair.run_for_rotations(4,-50,50)
pair.stop()
print("Stop moving forward")
#stay for 3second:
time.sleep(.5)

#go backward :::
pair.run_for_rotations(4, 50,-50)
pair.stop()
time.sleep(.5)


##### Turn 90 degree left:::::

count=0
while(count<4):
#turn 90degrees left and move
	print(f"turn{count} start here::")
	pair.run_for_rotations(.85,50,50)
	pair.stop()
	time.sleep(1.5)
	print("Motor turns and ready to go")

	pair.run_for_rotations(3,-50,50)
	pair.stop()
	print("Motor Stop")
	time.sleep(1.5)
	count +=1


