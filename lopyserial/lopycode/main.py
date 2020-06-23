# LoRa Serial Proxy (lsp.py)
# based on https://github.com/pmanzoni/loractp
# PM apr 2020

import binascii
import hashlib
import machine
import network
import pycom
import socket
import struct
import sys
import time
import ujson
from network import LoRa

import ufun
import iouart0

pycom.heartbeat(False) 


MAX_PKT_SIZE = 222  # Maximum pkt size in LoRa with Spread Factor 7  (¿230?)
HEADER_SIZE  = 20
PAYLOAD_SIZE = MAX_PKT_SIZE - HEADER_SIZE

lora = LoRa(mode = LoRa.LORA,
        frequency    = 868000000,
        tx_power     = 14,
        bandwidth    = LoRa.BW_125KHZ,
        sf           = 7,
        preamble     = 8,
        coding_rate  = LoRa.CODING_4_5,
        power_mode   = LoRa.ALWAYS_ON,
        tx_iq        = False,
        rx_iq        = False,
        public       = True,
        tx_retries   = 1,
        device_class = LoRa.CLASS_A)

loramac = binascii.hexlify(network.LoRa().mac())
print("lsp: loralmac = ", loramac)

try: 
    lorasoc = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lorasoc.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
except:
    print("DISASTER: cannot open LoRa socket")
print("lsp: created lorasoc")

# Just in case connected to the LoPy REPL via USB
ufun.flash_led_to(ufun.RED,3)

# Handling incoming data from UART0

# connecting to UART0
ufun.set_led_to(ufun.GREEN)
try:
    iouart0.connect()
except Exception as e:
    print("cannot connect to UART0")
time.sleep(1)
ufun.set_led_to(ufun.OFF)
# waiting commands via UART0

while True:
    dlen , b = iouart0.read()

    if dlen == 0:
        io0writestatus("ERROR1", "iouart0.read() returned 0 lentgh buffer")

    elif b.startswith(b"TEST"):
        iouart0.write(b"LINE_TEST_OK")

    elif b.startswith(b"CONNECT"):
        iouart0.write(b"OKCONNECTED")

    elif b.startswith(b"getloramac"):
        iouart0.write(loramac)

    elif b.startswith(b"settimeout"):
        t = struct.unpack("f", b[10:])[0]
        lorasoc.settimeout(t)
        iouart0.write("ok")

    elif b.startswith(b"SR"):    # send and receive ACK
        packet = b[2:]
        try:
            lorasoc.setblocking(True)
            lorasoc.send(packet)
            # waiting for the ack
            ack = lorasoc.recv(HEADER_SIZE)
        except lorasoc.timeout:
            ack = b"socket.timeout"
        iouart0.write(ack)

    elif b.startswith(b"S"):    # send
        packet = b[1:]
        lorasoc.setblocking(False)
        lorasoc.send(packet)
        iouart0.write("sack")

    elif b.startswith(b"R"):    # receive
        try:
            lorasoc.setblocking(True)
            r = lorasoc.recv(MAX_PKT_SIZE)
        except lorasoc.timeout:
            r = b"socket.timeout"
        iouart0.write(r)

    else:
        # iouart0.write("ERROR0: got..."+str(b)+"...-..."+str(dlen))
        ufun.flash_led_to(ufun.RED)
