#!/usr/bin/env python

import time
import serial
import threading
import sys
import datetime

def wait_cmd(ser, event):

    while not event.is_set():
        received_data = ser.readline()  # read serial port
        ser.flush()
        idx = received_data.decode('utf-8').find('\n')
        if 'Start new cycle!' in received_data[:idx].decode('utf-8'):
            event.set()
            print('{} :: hearing_side_cam :: wait_cmd :: Top motor is done!'.format(str(datetime.datetime.now())))
            break
        time.sleep(1)

ser = serial.Serial(

    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

event = threading.Event()
thd = threading.Thread(target=wait_cmd, args=(ser, event))

timestamp = sys.argv[1]
msg = 'New cycle has started!' + '-' + timestamp + '\n'
print(msg)
ser.write(msg.encode('utf-8'))
time.sleep(1)
ser.flush()

thd.start()
thd.join()