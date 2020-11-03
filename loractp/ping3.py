import time
import gc
import ujson
import math
import ucrypto
import loractp

gc.enable()

ctpc = loractp.CTPendpoint()

myaddr, rcvraddr, quality, result = ctpc.connect()
if (result == 0):
	print("ping.py: connected to {} (myaddr = {}, quality {})".format(rcvraddr, myaddr, quality))
else:
	print("ping.py: failed connection to {} (myaddr = {}, quality {})".format(rcvraddr, myaddr, quality))

time.sleep(1)

while True:

	msg = str(input("Message to be sent: "))

	t0 = time.time()
	tbs_ = {"type": "PING", "value": msg, "time": time.time()}
	tbsj = ujson.dumps(tbs_)
	tbsb = str.encode(tbsj)
	try:
		addr, quality, result = ctpc.sendit(rcvraddr, tbsb)
		print("ping.py: ACK from {} (quality = {}, result {})".format(addr, quality, result))
	except Exception as e:
		print ("ping.py: EXCEPTION when sending -> ", e)
		break

	print('ping.py: waiting pong from: ', rcvraddr)
	try:
		rcvd_data, addr = ctpc.recvit(rcvraddr)
		print("ping.py: pong {} from {}".format(rcvd_data, addr))
	except Exception as e:
		print ("ping.py: EXCEPTION when receiving ->", e)
		break
	t1 = time.time()
	print ("ping.py: elapsed time = ", t1-t0)

	tbs = ""
	tbsj = ""
	tbsb = ""
	gc.collect()

	if input("Q to exit: ") == "Q": break