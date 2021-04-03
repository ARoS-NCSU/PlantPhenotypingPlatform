#!/usr/bin/env python
'''
This is file is ran by the top motor and is triggered by node-red after a reset or camera capture by the top motor
'''
import time
import serial

ser = serial.Serial(

    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

msg = 'Start new cycle!' + '\n'
ser.write(msg.encode('utf-8'))