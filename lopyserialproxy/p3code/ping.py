import time
import json
import random

import lsp.loractp as loractp

ctpc = loractp.CTPendpoint()

myaddr, rcvraddr, quality, result = ctpc.connect()
if (result == 0):
    print("connected from {} to {} quality {}".format(myaddr, rcvraddr, quality))
else:
    print("failed connection from {} to {} quality {}".format(myaddr, rcvraddr, quality))

time.sleep(2)

while True:

    tbs_ = {"type": "PING", "value": random.randint(1,100), "time": time.time()}
    tbsj = json.dumps(tbs_)
    tbsb = str.encode(tbsj)
    print('ping.py: sending ', tbsb)
    try:
        addr, quality, result = ctpc.sendit(rcvraddr, tbsb)
        print("ping.py: got ", addr, quality, result)
    except Exception as e:
        print ("ping.py: EXCEPTION!! ", e)
        break

    print('ping.py: waiting for data from ', rcvraddr)
    try:
        rcvd_data, addr = ctpc.recvit(rcvraddr)
        print("ping.py: got ", rcvd_data, addr)
    except Exception as e:
        print ("ping.py: EXCEPTION!! ", e)
        break

    q = input("Q to exit: ")
    if q == "Q": break




