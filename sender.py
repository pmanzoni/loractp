import time
import sys
import loractp

def send_it(tbs_bytes):
#    tbs_bytes = str.encode(tbs)
    print('client.py: sending: ', tbs_bytes)
    try:
        addr, quality, result = ctpc.write(rcvraddr, tbs_bytes)
        print("client.py: got: ", addr, quality, result)
    except Exception as e:
        print ("client.py: EXCEPTION!! ", e)
        sys.exit(2)
    time.sleep(3)


ctpc = loractp.CTPendpoint()

myaddr, rcvraddr, quality, result = ctpc.connect()
if (result == 0):
    print("connected from {} to {} quality {}".format(myaddr, rcvraddr, quality))
else:
    print("failed connection from {} to {} quality {}".format(myaddr, rcvraddr, quality))
time.sleep(3)

tbs = b'\x00'
send_it(tbs)

tbs = b'1'
send_it(tbs)

tbs = b'\x06'   # ASCII ACK
send_it(tbs)

tbs = b'Hi, this is a msg from pietro and by the way is exactly 202 bytes long which is the size of a packet in the loractp library. I repeat, this is a msg from pietro and by the way is exactly 202 bytes long.'
send_it(tbs)

tbs = b"Ciao, questo è un messaggio da pietro ed è esattamente lungo 226 byte, che è maggiore della dimensione di un pacchetto nella libreria loractp. Ripeto, questo è un messaggio da pietro e tra l'altro è lungo esattamente 226 byte."
send_it(tbs)

