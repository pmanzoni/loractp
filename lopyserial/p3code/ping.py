import time
import json
import random

import config
import lsp.loractp as loractp

ctpc = loractp.CTPendpoint(port=config.serial_port)

# connect(dest=ANY_ADDR):
# - by default it tries to connect to a LoRa device that it's "listening" 
# returns:
# - myaddr = my Lora device MAC address (shortened)
# - rcvraddr = MAC address (shortened) of the Lora device we connected to
# - quality = the higher the worst, number of retransmissions 
# - result = etiher 0 (connected) or -1 (failed)
myaddr, rcvraddr, quality, result = ctpc.connect()
if (result == 0):
    print("ping.py: connected to {} (myaddr = {}, quality {})".format(rcvraddr, myaddr, quality))
else:
    print("ping.py: failed connection to {} (myaddr = {}, quality {})".format(rcvraddr, myaddr, quality))

time.sleep(1)

while True:

    t0 = time.time()
    tbs_ = {"type": "PING", "value": random.randint(1,100), "time": time.time()}
    tbsj = json.dumps(tbs_)
    tbsb = str.encode(tbsj)
    print('ping.py: sending ', tbsb)
    try:
        # sendit(addr=ANY_ADDR, payload=b''):
        # - by default it tries to send "payload" to any receiving LoRa device
        # --> in this example we are sending back to the device that we connected with
        # returns:
        # - addr = MAC address (shortened) of the Lora device that replies
        # - quality = the higher the worst, number of retransmissions 
        # - result = etiher 0 (connected) or -1 (failed)
        addr, quality, result = ctpc.sendit(rcvraddr, tbsb)
        print("ping.py: ACK from {} (quality = {}, result {})".format(addr, quality, result))
    except Exception as e:
        print ("ping.py: EXCEPTION when sending -> ", e)
        break

    print('ping.py: waiting pong from: ', rcvraddr)
    try:
        # recvit(addr=ANY_ADDR):
        # - by default it waits to receive data from any LoRa device
        # --> in this example we are waiting for data from the device that we connected with
        # returns:
        # - rcvd_data = that data itself
        # - addr = MAC address (shortened) of the Lora device that sent the data
        rcvd_data, addr = ctpc.recvit(rcvraddr)
        print("ping.py: pong {} from {}".format(rcvd_data, addr))
    except Exception as e:
        print ("ping.py: EXCEPTION when receiving ->", e)
        break
    t1 = time.time()
    print ("ping.py: elapsed time = ", t1-t0)


    if input("Q to exit: ") == "Q": break




