import json
import math
import random
import time

import config
import lsp.loractp as loractp


def random_in_range(l=0,h=1000):
    random.randrange(l,h)

ctpc = loractp.CTPendpoint(port=config.serial_port)

myaddr, rcvraddr, status = ctpc.listen()
if (status == 0):
    print("pong.py: connection from {} to me ({})".format(rcvraddr, myaddr))
else:
    print("pong.py: failed connection from {} to me ({})".format(rcvraddr, myaddr))

while True:

    print('pong.py: waiting for data from ', rcvraddr)
    try:
        rcvd_data, addr = ctpc.recvit(rcvraddr)
        print("pong.py: got ", rcvd_data, addr)
    except Exception as e:
        print ("pong.py: EXCEPTION!! ", e)
        break

    tbs = {"type": "PONG", "value": random_in_range(), "time": time.time()}
    tbsj = json.dumps(tbs)
    tbsb = str.encode(tbsj)
    print('pong.py: sending ', tbsb)
    try:
        addr, quality, result = ctpc.sendit(rcvraddr, tbsb)
        print("pong.py: ACK from {} (quality = {}, result = {})".format(addr, quality, result))
    except Exception as e:
        print ("pong.py: EXCEPTION!! ", e)
        break
