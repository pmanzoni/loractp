import time
import loractp

ctpc = loractp.CTPendpoint()

myaddr, rcvraddr, quality, result = ctpc.connect()
if (result == 0):
    print("connected from {} to {} quality {}".format(myaddr, rcvraddr, quality))
else:
    print("failed connection from {} to {} quality {}".format(myaddr, rcvraddr, quality))

time.sleep(3)

icount = 0
while icount < 2:
    tbs = '.msg from pietro ' + str(icount) + " is this."
    tbs_bytes = str.encode(tbs)
    print('client.py: sending: ', tbs_bytes)
    try:
        addr, quality, result = ctpc.write(rcvraddr, tbs_bytes)

        print("client.py: got: ", addr, quality, result)
        icount += 1
        time.sleep(3)
    except Exception as e:
        print ("client.py: EXCEPTION!! ", e)
        break
