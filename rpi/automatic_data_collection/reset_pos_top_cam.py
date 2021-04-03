#!/usr/bin/ python
# Based on the code of:
# Copyright (c) 2017-2025 John R. Leeman
# Distributed under the terms of the MIT License.
# Changed by Rafael L. da Silva, Sep 14th, 2019.

from time import sleep
import sys
import time
import RPi.GPIO as GPIO
import threading
import os
import time
import datetime
import signal
import utils


def read_switch():

    counter = 0
    while not event.is_set():
        end_of_course = not GPIO.input(20)
        if (switch_stuck.is_set() and end_of_course) is True:
            print('{} :: reset_top_cam :: Limit switch seems to be stuck...\n'.format(str(datetime.datetime.now())))
            away_only.set()
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
    motor.disable()
    GPIO.cleanup()
    time.sleep(0.5)
    print('Command executed.')


if __name__ == '__main__':

    # initialize the connections
    main_pid = os.getpid()

    # Switch pins configuration
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button to BCM 20

    # Switch monitoring in a separate thread
    monitor_switch = threading.Thread(target=read_switch, )
    event = threading.Event()
    away_only = threading.Event()
    switch_stuck = threading.Event()
    switch_stuck.set()
    monitor_switch.start()

    # Stepper motor configuration
    enable_pin = 5
    MS1_pin = 6
    MS2_pin = 13
    MS3_pin = 19
    direction_pin = 26
    step_pin = 16
    pins = [enable_pin, MS1_pin, MS2_pin, MS3_pin, direction_pin, step_pin]
    motor = utils.configure_rpi2stepper(pins)

    # Allow some time to the thread figure out if the camera is stuck at the switch or not
    sleep(0.1)
    switch_stuck.clear()

    reset_steps = 19
    print('{} :: reset_top_cam :: top camera position reset started.'.format(str(datetime.datetime.now())))

    try:
        # if limit switch has been reached
        if away_only.is_set():
            pass
        else:
            # This is away from motor direction
            motor.set_direction('cw')
            print(motor.move_degrees(reset_steps * 360, dynamic_stepsize=False))
            time.sleep(10)
        print('{} :: reset_top_cam :: top camera position reset finished.'.format(str(datetime.datetime.now())))
        print('------------')
        wrapup()

    except KeyboardInterrupt:

        wrapup()
