# Copyright (c) 2017-2025 John R. Leeman
# Distributed under the terms of the MIT License.
# Copied from https://github.com/jrleeman/windicator/blob/master/src/bigeasydriver.py
"""Control the Big Easy Driver (BED)
Contains tools to control stepper motors with the Big Easy Driver by Brian
Schmalz. For more information on the BED visit www.schmalzhaus.com/BigEasyDriver
"""
from math import floor

import RPi.GPIO as GPIO
from time import sleep

class BigEasyDriver(object):
    r"""The Big Easy Driver.
    This class contains information on connections and control methods for the
    BED.
    """

    def __init__(self):
        # Hardware pin connections
        self.enable_pin = None
        self.MS1_pin = None
        self.MS2_pin = None
        self.MS3_pin = None
        self.reset_pin = None
        self.sleep_pin = None
        self.step_pin = None
        self.direction_pin = None

        # Hardware state information
        self.isenabled = True
        self.direction = 'ccw'
        self.step_size = 'sixteenth step'
        self.isasleep = False
        self.isinreset = False
        self.microsteps_per_step = 16

        # Motor information
        self.degrees_per_step = None


    def begin(self):
        """
        Actually initialze the hardware pin states once they are set.
        """
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        if self.enable_pin is not None:
            GPIO.setup(self.enable_pin, GPIO.OUT)
            GPIO.output(self.enable_pin, GPIO.LOW)
        if self.MS1_pin is not None:
            GPIO.setup(self.MS1_pin, GPIO.OUT)
            GPIO.output(self.MS1_pin, GPIO.HIGH)
        if self.MS2_pin is not None:
            GPIO.setup(self.MS2_pin, GPIO.OUT)
            GPIO.output(self.MS2_pin, GPIO.HIGH)
        if self.MS3_pin is not None:
            GPIO.setup(self.MS3_pin, GPIO.OUT)
            GPIO.output(self.MS3_pin, GPIO.HIGH)
        if self.reset_pin is not None:
            GPIO.setup(self.reset_pin, GPIO.OUT)
            GPIO.output(self.reset_pin, GPIO.HIGH)
        if self.sleep_pin is not None:
            GPIO.setup(self.sleep_pin, GPIO.OUT)
            GPIO.output(self.sleep_pin, GPIO.HIGH)
        if self.step_pin is not None:
            GPIO.setup(self.step_pin, GPIO.OUT)
            GPIO.output(self.step_pin, GPIO.HIGH)
        if self.direction_pin is not None:
            GPIO.setup(self.direction_pin, GPIO.OUT)
            GPIO.output(self.direction_pin, GPIO.HIGH)


    def enable(self):
        """
        Enable the BED driver chip and final drive circuits.
        """
        # Enabled when enable is low. There is a 20k pulldown on the BED, so we
        # can let it float or pull it low. I chose to pull it low.
        GPIO.output(self.enable_pin, GPIO.LOW)
        self.isenabled = True
        return True

    def disable(self):
        """
        Disable the BED final drive ciruits.
        """
        GPIO.output(self.enable_pin, GPIO.HIGH)
        self.isenabled = False
        return True


    def set_stepsize(self, step_size):
        """
        Set the step size the motor will take.
        Options: full step, half step, quarter step, eigth step, sixteenth step
        """
        self.step_size = step_size
        microstep_pins = [self.MS1_pin, self.MS2_pin, self.MS3_pin]

        microstep_pin_states = {'full step': [GPIO.LOW, GPIO.LOW, GPIO.LOW],
                                'half step': [GPIO.HIGH, GPIO.LOW, GPIO.LOW],
                                'quarter step': [GPIO.LOW, GPIO.HIGH, GPIO.LOW],
                                'eigth step': [GPIO.HIGH, GPIO.HIGH, GPIO.LOW],
                                'sixteenth step': [GPIO.HIGH, GPIO.HIGH, GPIO.HIGH]}

        microsteps_per_step = {'full step': 1, 'half step': 2, 'quarter step':4,
                               'eigth step': 8, 'sixteenth step':16}

        try:
            microstep_states = microstep_pin_states[self.step_size]
            self.step_size = step_size
            self.microsteps_per_step = microsteps_per_step[self.step_size]
        except KeyError:
            raise ValueError('Unkown option for step_size: {0}'.format(self.step_size))

        # Actually toggle the outputs
        for pin, state in zip(microstep_pins, microstep_states):
            GPIO.output(microstep_pins, microstep_states)

        return True


    def set_direction(self, direction):
        """
        Set the direction of motor rotation.
        Input is tied high on the BED
        """
        direction_pin_states = {'ccw': GPIO.HIGH,
                                'cw': GPIO.LOW}
        try:
            direction_state = direction_pin_states[direction]
            self.direction = direction
        except KeyError:
            raise ValueError('Unknown direction: {0}'.format(direction))

        # Actually set the pin state
        GPIO.output(self.direction_pin, direction_state)
        return True


    def step(self):
        """
        Move the motor by one step.
        Motor steps on the rising edge on the rising edge. The pulse must be at
        least 1us high and 1us low.
        """
        GPIO.output(self.step_pin, GPIO.LOW)
        sleep(3e-3)
        GPIO.output(self.step_pin, GPIO.HIGH)
        sleep(3e-3)
        return True


    def move_nsteps(self, nsteps):
        """
        Move the motor by nsteps.
        Motor steps on the rising edge on the rising edge. The pulse must be at
        least 1us high and 1us low.
        """
        for i in range(nsteps):
            self.step()
        return True

    def move_degrees(self, degrees, dynamic_stepsize=False):
        """
        Move the motor a specified number of degrees.
        Returns the acutal amount moved.
        """
        if dynamic_stepsize:
            total_degrees_moved = 0.
            initial_stepsize = self.step_size
            # Start with full steps
            self.set_stepsize('full step')
            nsteps = int(floor((degrees - total_degrees_moved)/ (self.degrees_per_step / self.microsteps_per_step)))
            print("steos: ", nsteps, self.microsteps_per_step)
            self.move_nsteps(nsteps)
            total_degrees_moved += nsteps * (self.degrees_per_step / self.microsteps_per_step)
            print("moved: ", total_degrees_moved)
            
            # Half steps
            self.set_stepsize('half step')
            nsteps = int(floor((degrees - total_degrees_moved)/ (self.degrees_per_step / self.microsteps_per_step)))
            self.move_nsteps(nsteps)
            print("steos: ", nsteps, self.microsteps_per_step)
            total_degrees_moved += nsteps * (self.degrees_per_step / self.microsteps_per_step)
            print("moved: ", total_degrees_moved)

            # Quarter steps
            self.set_stepsize('quarter step')
            nsteps = int(floor((degrees - total_degrees_moved)/ (self.degrees_per_step / self.microsteps_per_step)))
            self.move_nsteps(nsteps)
            print("steos: ", nsteps, self.microsteps_per_step)
            total_degrees_moved += nsteps * (self.degrees_per_step / self.microsteps_per_step)
            print("moved: ", total_degrees_moved)
        
            # Eigth steps
            self.set_stepsize('eigth step')
            nsteps = int(floor((degrees - total_degrees_moved)/ (self.degrees_per_step / self.microsteps_per_step)))
            self.move_nsteps(nsteps)
            print("steos: ", nsteps, self.microsteps_per_step)
            total_degrees_moved += nsteps * (self.degrees_per_step / self.microsteps_per_step)
            print("moved: ", total_degrees_moved)
            
            # Sixteenth steps
            self.set_stepsize('sixteenth step')
            nsteps = int(floor((degrees - total_degrees_moved)/ (self.degrees_per_step / self.microsteps_per_step)))
            self.move_nsteps(nsteps)
            print("steos: ", nsteps, self.microsteps_per_step)
            total_degrees_moved += nsteps * (self.degrees_per_step / self.microsteps_per_step)
            print("moved: ", total_degrees_moved)
            
            # Go back to the stepsize we had upon entry
            self.set_stepsize(initial_stepsize)

            return total_degrees_moved

        else:
            nsteps = int(floor(degrees / self.degrees_per_step * self.microsteps_per_step))
            self.move_nsteps(nsteps)
            return nsteps / self.microsteps_per_step * self.degrees_per_step
