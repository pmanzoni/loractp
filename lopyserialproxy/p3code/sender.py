import time
import sys
import loractp

def send_it(tbs_bytes):
#    tbs_bytes = str.encode(tbs)
    print('client.py: sending: ', tbs_bytes)
    try:
        addr, quality, result = ctpc.sendit(rcvraddr, tbs_bytes)
        print("client.py: got: ", addr, quality, result)
    except Exception as e:
        print ("client.py: EXCEPTION!! ", e)
        sys.exit(2)


ctpc = loractp.CTPendpoint(port='/dev/ttyACM0')

myaddr, rcvraddr, quality, result = ctpc.connect()
if (result == 0):
    print("connected from {} to {} quality {}".format(myaddr, rcvraddr, quality))
else:
    print("failed connection from {} to {} quality {}".format(myaddr, rcvraddr, quality))
time.sleep(3)

# tbs = b'\x00'
# send_it(tbs)
# time.sleep(3)

tbs = b'hola'
send_it(tbs)
time.sleep(2)

# tbs = b'\x06'   # ASCII ACK
# send_it(tbs)
# time.sleep(3)



tbs = b'Hi, this is a msg from pietro and by the way is exactly 202 bytes long which is the size of a packet in the loractp library. I repeat, this is a msg from pietro and by the way is exactly 202 bytes long.'
send_it(tbs)
time.sleep(2)

tbs = b'Hi, this is a msg from pietro and by the way is exactly 210 bytes long which is longer than the size of a packet in the loractp library. I repeat, this is a msg from pietro and it is exactly 210 bytes long.XYWZ'
send_it(tbs)
