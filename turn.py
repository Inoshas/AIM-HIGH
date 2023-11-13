from buildhat import MotorPair
import time

pair = MotorPair('A','B')

pair._leftmotor.set_default_speed(-60)
pair._leftmotor.set_default_speed(60)

#turn sharp
#pair.run_for_seconds(.5, 50, 50)



#turn shallow
count = 0
while count < 4:
	pair.run_for_rotations(3, -50, 50)
	pair.run_for_rotations(4.5, 0, 100)
#	pair.run_for_rotations(3, -100, 0)
	count += 1


