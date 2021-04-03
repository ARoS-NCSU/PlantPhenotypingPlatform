# Copyright (c) 2017-2025 John R. Leeman
# Distributed under the terms of the MIT License.

from time import sleep

import bigeasydriver
import RPi.GPIO as GPIO

stepper = bigeasydriver.BigEasyDriver()
stepper.enable_pin = 5
stepper.MS1_pin = 6
stepper.MS2_pin = 13
stepper.MS3_pin = 19
stepper.direction_pin = 26
stepper.step_pin = 16

stepper.begin()
stepper.degrees_per_step = 1.8
stepper.set_stepsize('full step')

import numpy as np

for i in range(10):
    deg = np.random.random_integers(0, 360)
    stepper.set_direction('cw')
    sleep(0.1)
    print(stepper.move_degrees(deg, dynamic_stepsize=False))
    stepper.set_direction('ccw')
    sleep(0.1)
    print(stepper.move_degrees(deg, dynamic_stepsize=False))
    

stepper.disable()
while True:
    sleep(1)

stepper.set_direction('ccw')
stepper.set_stepsize('full step')
print("Moving CCW")
stepper.move_nsteps(1000)
sleep(0.5)
print("Moving CW")
stepper.set_direction('cw')
stepper.move_nsteps(1000)
sleep(1)
print(stepper.move_degrees(25, dynamic_stepsize=True))
sleep(1)
print(stepper.move_degrees(90))
sleep(1)
print(stepper.move_degrees(18.5, dynamic_stepsize=True))
for i in range(10):
    sleep(1)
    print(stepper.move_degrees(5., dynamic_stepsize=True))


stepper.disable()