import time
import loractp

VERBOSE = True

ANY_ADDR = b'\x00\x00\x00\x00\x00\x00\x00\x00'

ctpc = loractp.CTPendpoint()

myaddr, rcvraddr, status = ctpc.listen()

if (status == 0):
    print("connection from {} to me ({})".format(rcvraddr, myaddr))
else:
    print("failed connection from {} to me ({})".format(rcvraddr, myaddr))

while True:
    print('receiver.py: waiting for data from : ', rcvraddr)
    try:
        rcvd_data, addr = ctpc.read(rcvraddr)
        print("receiver.py: got: ", rcvd_data, addr)
    except Exception as e:
        print ("receiver.py: EXCEPTION!! ", e)
        break
