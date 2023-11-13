import time

from buildhat import Motor, MotorPair

#Define motor pair:

pair = MotorPair('A', 'B')
#Run forward for 3 rotations::
pair.run_for_rotations(3, -50, 50)
print("forward")
#stay for 3second:
time.sleep(.5)

#go backword :::
pair.run_for_seconds(3, 50,-50)


time.sleep(.5)
#turn 90degrees left
#pair.run_for_degrees(90,-50,50)
print("turn")
pair.run_for_seconds(1,-12,100)
pair.stop()
time.sleep(.5)
pair.run_for_seconds(3,-50,50)
pair.stop()
time.sleep(.5)

#turn 90degrees right
#pair.run_for_degrees(90,-50,50)
#print("turn")
pair.run_for_seconds(1,12,-100)
pair.stop()
time.sleep(.5)
pair.run_for_seconds(3,-50,50)
pair.stop()

