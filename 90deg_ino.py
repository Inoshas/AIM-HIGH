
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

#set motors  default values:::
pair._leftmotor.set_default_speed(-60)
pair._rightmotor.set_default_speed(60)

##Print left and right motor values

pair._leftmotor.when_rotated = handle_motor
print("********")
pair._rightmotor.when_rotated =handle_motor
print("######")

pair.start()
#pair.run_for_seconds(1, 100,-100)
print("Forward moving start here----")
#Run forward for 3 rotations::
pair.run_for_seconds(4,-50,50)
pair.stop()
print("Stop moving forward")
#stay for 3second:
time.sleep(.5)

#go backward :::
pair.run_for_seconds(10, 50,-50)
pair.stop()
time.sleep(.5)



'''
count=0
while(count<1):
#turn 90degrees left and move
	print(f"turn{count} start here::")
	pair.run_for_seconds(2.5,0,100)
	pair.stop()
	time.sleep(1.5)
	print("Motor turns and ready to go")
#	pair.run_for_seconds(.5,-10,0)
#	pair.stop()
#	time.sleep(1.5)
	pair.run_for_seconds(3,-50,50)
	pair.stop()
	print("Motor Stop")
	time.sleep(1.5)
	count +=1

"""

#turn 90degrees right
#pair.run_for_degrees(90,-50,50)
print("turn")
pair.run_for_seconds(1,100,-10)
pair.stop()
time.sleep(.5)
pair.run_for_seconds(1,100,-10)
pair.stop()
time.sleep(.5)
pair.run_for_seconds(3,-50,50)
pair.stop()
time.sleep(.5)
"""
'''
