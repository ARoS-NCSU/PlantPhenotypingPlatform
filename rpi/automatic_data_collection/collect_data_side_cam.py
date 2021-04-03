#!/usr/bin/ python
# Based on the code of:
# Copyright (c) 2017-2025 John R. Leeman
# Distributed under the terms of the MIT License.
# Changed by Rafael L. da Silva, Oct 20th, 2019.

from time import sleep
import sys
import time
import RPi.GPIO as GPIO
import threading
import os
import time
import datetime
import signal
from picamera import PiCamera
import serial
import utils
import collect_data_realsense as realsense


def read_switch():

    counter = 0
    while not event.is_set():
        end_of_course = not GPIO.input(20)
        if (switch_stuck.is_set() and end_of_course) is True:
            print('{} :: reset_side_cam :: Limit switch seems to be stuck...\n'.format(str(datetime.datetime.now())))
            UP_only.set()
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
    print('Command executed.')


def start_movement(step_size, idx, camera, path_picamera, path_realsense):

    global g, custom_gains, timestamp

    try:
        # This is UP direction
        motor.set_direction('cw')
        for k in range(0, int(total_steps//step_size)):
            print(motor.move_degrees(step_size * 360, dynamic_stepsize=False))
            time.sleep(0.5)
            #camera.awb_gains = custom_gains
            # Time required for the camera update gains
            #time.sleep(1)

            # True - use default realsense config, False - use custom config
            try:
                cmd = 'rs_filepath_command --path ' + path_realsense + '/res_' + timestamp + '_' + str(idx).zfill(6)
                os.system(cmd)
                print('{} :: collect_data_realsense :: taking picture {}.'.format(str(datetime.datetime.now()), idx))
            except:
                print('{} :: collect_data_side_cam :: Some problem happened with the RealSense camera!! x(')

            try:
                camera.capture(path_picamera + '/pic_' + timestamp + '_' + str(idx).zfill(6) + '.jpg')
                print('{} :: collect_data_side_cam :: taking picture {}.'.format(str(datetime.datetime.now()), idx))
            except:
                print('{} :: collect_data_side_cam :: Some problem happened with the camera!! x(')
            #camera.awb_gains = g
            # Time required for the camera update gains
            #time.sleep(1)
            #camera.capture(data_path + '/pic_awboff_' + timestamp + '_' + str(idx).zfill(6) + '.jpg')
            #print('{} :: collect_data_side_cam_awboff :: taking picture {}.'.format(str(datetime.datetime.now()), idx))
            idx += 1

        wrapup()

    except KeyboardInterrupt:

        wrapup()

if __name__ == '__main__':

    # Data ID label and formatting
    date_now = str(datetime.datetime.now()).replace(' ', '_')
    date_now = date_now.replace(':', '_')
    date_now = date_now.replace('.', '_')

    # It receives the string "timestamp path" from node-red
    argument = sys.argv[1]
    data_folder = sys.argv[2]
    timestamp = argument.replace(':', '_')
    timestamp = timestamp.replace('.', '_')

    # initialize the connections
    main_pid = os.getpid()
    # Switch pins configuration
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button to BCM 20

    # Switch monitoring in a separate thread

    monitor_switch = threading.Thread(target=read_switch,)
    event = threading.Event()
    UP_only = threading.Event()
    switch_stuck = threading.Event()
    switch_stuck.set()
    monitor_switch.start()
    event = threading.Event()

    # Stepper motor configuration
    enable_pin = 5
    MS1_pin = 6
    MS2_pin = 13
    MS3_pin = 19
    direction_pin = 26
    step_pin = 16
    pins = [enable_pin, MS1_pin, MS2_pin, MS3_pin, direction_pin, step_pin]
    motor = utils.configure_rpi2stepper(pins)
    step_size = 0.2
    total_steps = 6

    # Pictures directory routing
    subject_picamera = 'SideCam'
    subject_realsense = 'RealSense'
    trial = 'Trial008'
    data_path_picamera = utils.directory_manager(data_folder, date_now, subject_picamera, trial)
    data_path_realsense = utils.directory_manager(data_folder, date_now, subject_realsense, trial)
    idx = utils.get_next_pic_idx(data_folder, subject_picamera, trial, timestamp)
    # Allow some time to the thread figure out if the camera is stuck at the switch or not
    sleep(0.1)
    switch_stuck.clear()

    # Camera configuration
    camera = PiCamera(resolution=(3280, 2464))
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    camera.awb_mode = 'off'
    # Time required for the camera update gains
    time.sleep(1)
    #g = camera.awb_gains
    #print('{} :: collect_data_side_cam :: custom gains {}.'.format(str(datetime.datetime.now()), g))
    custom_gains = (1.9, 0.8)
    camera.awb_gains = custom_gains
    # Time required for the camera update gains
    time.sleep(1)
    print('{} :: collect_data_side_cam :: custom gains {}.'.format(str(datetime.datetime.now()), custom_gains))
    # Stepper movement
    start_movement(step_size, idx, camera, data_path_picamera, data_path_realsense)