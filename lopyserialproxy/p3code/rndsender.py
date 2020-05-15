import time
import json
import random

import lsp.loractp as loractp

ctpc = loractp.CTPendpoint()

time.sleep(1)

while True:

    tbs_ = {"type": "rndsender", "value": random.randint(1,100), "time": time.time()}
    tbsj = json.dumps(tbs_)
    tbsb = str.encode(tbsj)
    print('rndsender.py: sending ', tbsb)
    try:
        # sendit(addr=ANY_ADDR, payload=b''):
        # - by default it tries to send "payload" to any receiving LoRa device
        # returns:
        # - addr = MAC address (shortened) of the Lora device that replies
        # - quality = the higher the worst, number of retransmissions 
        # - result = etiher 0 (connected) or -1 (failed)
        addr, quality, result = ctpc.sendit(payload=tbsb)
        print("rndsender.py: ACK from {} (quality = {}, result {})".format(addr, quality, result))
    except Exception as e:
        print ("rndsender.py: EXCEPTION when sending -> ", e)
        break

    time.sleep(random.randint(1,5))