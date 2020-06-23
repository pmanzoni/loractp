# Some useful functions "ufun":

from network import WLAN
import machine
import math
import pycom
import sys
import time
import ucrypto

RED = 0xFF0000
YELLOW = 0xFFFF33
GREEN = 0x007F00
OFF = 0x000000

def random_in_range(l=0,h=1000):
    r1 = ucrypto.getrandbits(32)
    r2 = ((r1[0]<<24)+(r1[1]<<16)+(r1[2]<<8)+r1[3])/4294967295.0
    return math.floor(r2*h+l)

def set_led_to(color=GREEN):
    pycom.heartbeat(False) # Disable the heartbeat LED
    pycom.rgbled(color)

def flash_led_to(color=GREEN, t1=1):
    set_led_to(color)
    time.sleep(t1)
    set_led_to(OFF)
