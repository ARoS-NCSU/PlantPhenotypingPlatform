#!/usr/bin/env python
'''
Communication from Node-Red to Side motor to Top motor
This script starts from bootup using node-red
Top motor resets to away position, sends cmd to Side motor
Side motor waits cmd from Top motor
Finish this part
'''
import time
import serial
import datetime
import threading


def wait_cmd(ser, event):

    while not event.is_set():
        received_data = ser.read_until()  # read serial port
        ser.flush()
        idx = received_data.decode('utf-8').find('\n')
        if 'New cycle has started!' in received_data[:idx].decode('utf-8'):
            event.set()
            # print('{} :: hearing_top_cam :: wait_cmd :: Reset Top motor done!'.format(str(datetime.datetime.now())))
            # Print timestamp so that top motor can use for its pictures
            print(received_data.decode('utf-8'))
            print(received_data[:idx].decode('utf-8').split('-', 1)[1])
            break
        time.sleep(1)


if __name__ == '__main__':

    ser = serial.Serial(

        port='/dev/serial0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None
    )

    event = threading.Event()
    thd = threading.Thread(target=wait_cmd, args=(ser, event))
    thd.start()
    thd.join()

