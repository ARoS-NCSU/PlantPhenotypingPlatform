#!/usr/bin/ python
# Copyright (c) 2017-2025 John R. Leeman
# Distributed under the terms of the MIT License.

from time import sleep
import sys
import time
import bigeasydriver
import RPi.GPIO as GPIO
import threading
import os
import time
import signal


def read_switch():

    counter = 0
    while not event.is_set():
        end_of_course = not GPIO.input(20)
        if (switch_stuck.is_set() and end_of_course) is True:
            print('Limit switch seems to be stuck...\n')
            ccw_only.set()
            event.set()
        elif end_of_course is True:
            if counter < 2:
                finish_request()
            else:
                counter += 1
        elif counter != 0:
            counter = 0
        time.sleep(0.01)


def finish_request():
    print('Limit switch reached!!\n')
    os.kill(main_pid, signal.SIGINT)


def wrapup():
    print('Wrapping up...\n')
    event.set()
    stepper.disable()
    GPIO.cleanup()
    print('Command executed.')

if __name__ == '__main__':

    # initialize the connections
    main_pid = os.getpid()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button to BCM 20
    monitor_switch = threading.Thread(target=read_switch,)
    event = threading.Event()
    ccw_only = threading.Event()
    switch_stuck = threading.Event()
    switch_stuck.set()
    monitor_switch.start()

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

    cmd = ['CC', 0]
    # Case string came in correct order
    print(sys.argv[1])
    if sys.argv[1][1] == '"':
        print("First argument:{}\n".format(sys.argv[1][2:4]))
        cmd[0] = sys.argv[1][2:4]
        if sys.argv[1][6] == '"':
            print("Wrong second argument! - {}\n".format(sys.argv[1]))
        else:
            if sys.argv[1][7] == '.':
                print("Second argument:{}\n".format(sys.argv[1][6:9]))
                cmd[1] = sys.argv[1][6:9]
            else:
                print("Second argument:{}\n".format(sys.argv[1][6]))
                cmd[1] = sys.argv[1][6]
    # Case string came inverted        
    elif isinstance(int(sys.argv[1][1]), int) is True:
        if sys.argv[1][2] == '.':
            print('First argument:{}\n'.format(sys.argv[1][1:4]))
            cmd[1] = sys.argv[1][1:4]
            if sys.argv[1][5] != '"':
                print("Wrong second argument! - {}\n".format(sys.argv[1]))
                print("Wrong second argument! - {}\n".format(sys.argv[1][6]))
            else:
                print('Second argument:{}\n'.format(sys.argv[1][6:8]))
                cmd[0] = sys.argv[1][6:8]
        else:
            print('First argument:{}\n'.format(sys.argv[1][1]))
            cmd[1] = sys.argv[1][1]
            if sys.argv[1][3] != '"':
                print("Wrong second argument! - {}\n".format(sys.argv[1]))
            else:
                print('Second argument:{}\n'.format(sys.argv[1][4:6]))
                cmd[0] = sys.argv[1][4:6]
    else:
        print('Wrong command sequence!!\n')
    
    # Allow some time to the thread figure out if the camera is stuck at the switch or not
    sleep(0.1)
    switch_stuck.clear()
    
    try:
        
        if cmd[0] == 'CW':
            stepper.set_direction('ccw')
            print("Moving CW - Clockwise\n")            
        elif cmd[0] == 'CC':
            stepper.set_direction('cw')
            print("Moving CCW - Counter-Clockwise\n")

        sleep(0.1)
        
        if ccw_only.is_set() and cmd[0] == 'CW':
            print('Limit switch has been reached!! Please move the motor CC - Counter-Clockwise!\n')
            ccw_only.clear()
        else:
            print(stepper.move_degrees(float(cmd[1])*360, dynamic_stepsize=False))
        
        sleep(1)
        wrapup()
        
    except KeyboardInterrupt:
        
        wrapup()
