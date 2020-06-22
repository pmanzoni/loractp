import serial
import readline
import time

lopyuart = None

def _write(data):
    global lopyuart
    lopyuart.write(data)


def _close():
    global lopyuart
    lopyuart.close(lopyuart)


def _connect(port='/dev/ttyACM0', timeout=1):
    global lopyuart

    lopyuart = serial.Serial(port = port, 
                        baudrate  = 115200, 
                        bytesize  = serial.EIGHTBITS, 
                        parity    = serial.PARITY_NONE, 
                        stopbits  = serial.STOPBITS_ONE, 
                        timeout   = timeout)
    _write(b"CONNECT")
    # lopyuart.flushInput()
    # lopyuart.flushOutput()

def read_all(chunk_size=1000):
    global lopyuart

    read_buffer = b''
    while True:
        # Read in chunks. Each chunk will wait as long as specified by
        # timeout. Increase chunk_size to fail quicker
        byte_chunk = lopyuart.read(size=chunk_size)
        read_buffer += byte_chunk
        if (not len(byte_chunk) == chunk_size) and (len(byte_chunk) > 0):
            break

    return read_buffer

def connect(port='/dev/ttyACM0', timeout=1):
    _connect(port)                
    r = read_all()
    if r.startswith(b"OKCONNECTED"):
        return "connected to: " + port 
    else:
        return "ERROR connecting to: " + port 


def writeread(data):
    _write(data)
    time.sleep(0.1)
    r = read_all()

    return r


