import time
import loractp

import ujson
import ucrypto
import math
def random_in_range(l=0,h=1000):
    r1 = ucrypto.getrandbits(32)
    r2 = ((r1[0]<<24)+(r1[1]<<16)+(r1[2]<<8)+r1[3])/4294967295.0
    return math.floor(r2*h+l)


ctpc = loractp.CTPendpoint()

myaddr, rcvraddr, status = ctpc.listen()
if (status == 0):
    print("connection from {} to me ({})".format(rcvraddr, myaddr))
else:
    print("failed connection from {} to me ({})".format(rcvraddr, myaddr))

time.sleep(2)

while True:

    print('pong.py: waiting for data from ', rcvraddr)
    try:
        rcvd_data, addr = ctpc.recvit(rcvraddr)
        print("pong.py: got ", rcvd_data, addr)
    except Exception as e:
        print ("pong.py: EXCEPTION!! ", e)
        break

    tbs = {"type": "PONG", "value": random_in_range(), "time": time.time()}
    tbsj = ujson.dumps(tbs)
    tbsb = str.encode(tbsj)
    print('pong.py: sending ', tbsb)
    try:
        addr, quality, result = ctpc.sendit(rcvraddr, tbsb)
        print("pong.py: got ", addr, quality, result)
    except Exception as e:
        print ("pong.py: EXCEPTION!! ", e)
        break
