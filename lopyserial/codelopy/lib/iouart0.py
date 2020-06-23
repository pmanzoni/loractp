# Tiny lib to talk with a LoPy via UART0
# PM apr 2020


from machine import UART
import pycom
import time
import binascii
import uos

uart0 = None

def connect():
    global uart0
    uart0 = UART(0)
    uart0.init(baudrate=115200, bits=8, parity=None, stop=1)
    uos.dupterm(uart0)


def read():
    global uart0
    bufstore = bytearray(1000)
    buffit   = memoryview(bufstore)
    while True:
        if not uart0.any():
            time.sleep(0.1)
        else:
            dlen = uart0.readinto(buffit)
            return dlen, bytes(buffit[0:dlen])


def write(data):
    global uart0
    buffit = memoryview(data)
    return uart0.write(buffit)

