"""
LoRa CTP (Content Transfer Protocol)
based on stop & wait like protocol and adapted to a LoRa raw channel

Tested on a LoPy4 quadruple bearer MicroPython enabled development board.

Inspired by https://github.com/arturenault/reliable-transport-protocol by Artur Upton Renault

First version by: Pietro GRC dic2017
Modified by: Pietro GRC apr2020
"""

import binascii
import hashlib
import struct
import sys
import time

from lsp import seriallopy

__version__ = '0'


class CTPendpoint:

    # Set to True for debugging messages
    DEBUG_MODE = False
    HARD_DEBUG_MODE = False

    MAX_PKT_SIZE = 222  # Maximum pkt size in LoRa with Spread Factor 7  (maybe 230???)
    HEADER_SIZE  = 20
    PAYLOAD_SIZE = MAX_PKT_SIZE - HEADER_SIZE
    # header structure:
    # 8 bytes: source addr (last 8 bytes)
    # 8 bytes: dest addr (last 8 bytes)
    # 1 byte: flags
    # 3 bytes: checksum
    HEADER_FORMAT  = "!8s8sB3s"
    PAYLOAD_FORMAT = "!202s"

    ITS_DATA_PACKET = False
    ITS_ACK_PACKET  = True
    ANY_ADDR = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    ONE  = 1
    ZERO = 0

    def __init__(self, port='/dev/ttyACM0'):

        r = seriallopy.connect(port)                
        print("loractp:", r)
        if r.startswith("ERROR"): sys.exit()

        if self.DEBUG_MODE: print(seriallopy.writeread(b"TEST"))

        # Get lora mac address
        r = seriallopy.writeread(b"getloramac")
        self.lora_mac = r
        self.my_addr  = self.lora_mac[8:]

        if self.DEBUG_MODE: print("lora_mac: ", self.lora_mac)
        print("loractp: my_addr = ", self.my_addr)

    #
    # BEGIN: Utility functions
    #

    # Create a packet from the necessary parameters
    def __make_packet(self, s_addr, d_addr, seqnum, acknum, pkt_type, is_last, content):
        # s_addr: bytes, d_addr: bytes, seqnum: int, acknum: int, pkt_type: boolean, is_last: boolean, content: bytes
        if self.HARD_DEBUG_MODE: print("DEBUG 049:", s_addr, d_addr, seqnum, acknum, pkt_type, is_last, content)
        flags = 0
        if seqnum == self.ONE:
            flags = flags | (1<<0)
        if acknum == self.ONE:
            flags = flags | (1<<2)
        if is_last:
            flags = flags | (1<<4)
        if pkt_type == self.ITS_ACK_PACKET:
            flags = flags | (1<<6)

        if (len(content)>0 and (pkt_type == self.ITS_DATA_PACKET)):
            # p = struct.pack(self.PAYLOAD_FORMAT, content)
            p = content
            check = self.__get_checksum(p)
            h = struct.pack(self.HEADER_FORMAT, s_addr, d_addr, flags, check)
            if self.HARD_DEBUG_MODE: print("DEBUG 065:", h+p)
        else:
            p = b''
            h = struct.pack(self.HEADER_FORMAT, s_addr, d_addr, flags, b'')
            if self.HARD_DEBUG_MODE: print("DEBUG 069:", h+p)

        return h + p

    # Break a packet into its component parts
    def __unpack(self, packet):
        header  = packet[:self.HEADER_SIZE]
        content = packet[self.HEADER_SIZE:]

        sp, dp, flags, check = struct.unpack(self.HEADER_FORMAT, header)
        seqnum   = self.ONE if ((flags) & 1) & 1 else self.ZERO
        acknum   = self.ONE if (flags >> 2)  & 1 else self.ZERO
        is_last  = (flags >> 4) & 1 == 1
        pkt_type = (flags >> 6) & 1 == 1
        if (content == b''):
            payload = b''
        else:
            payload = content
        return sp, dp, seqnum, acknum, pkt_type, is_last, check, payload

    def __get_checksum(self, data):
        # data: byte -> byte:
        if self.HARD_DEBUG_MODE: print("DEBUG 092: in get_checksum->", data)
        h = hashlib.sha256(data)
        ha = binascii.hexlify(h.digest())
        if self.HARD_DEBUG_MODE: print("DEBUG 095: in get_checksum->", ha[-3:])
        return (ha[-3:])

    def __debug_printpacket(self, msg, packet, cont=False):
        sp, dp, seqnum, acknum, pkt_type, is_last, check, content = self.__unpack(packet)
        if cont:
            print ("DEBUG {}: s_a: {}, d_a: {}, seqn: {}, ackn: {}, is-ack: {}, fin: {}, check: {}, cont: {}".format(msg, sp, dp, seqnum, acknum, pkt_type, is_last, check, content))
        else:
            print ("DEBUG {}: s_a: {}, d_a: {}, seqn: {}, ackn: {}, is_ack: {}, fin: {}, check: {}".format(msg, sp, dp, seqnum, acknum, pkt_type, is_last, check))

    def __timeout(self, signum, frame):
        raise socket.timeout

    #
    # END: Utility functions
    #

    def _csend(self, payload, sndr_addr, rcvr_addr):

        # Shortening addresses to last 8 bytes to save space in packet
        sndr_addr = sndr_addr[8:]
        rcvr_addr = rcvr_addr[8:]
        if self.DEBUG_MODE: print ("DEBUG 138: sndr_addr, rcvr_addr", sndr_addr, rcvr_addr)

        # computing payload (content) size as "totptbs" = total packets to be sent
        if (len(payload)==0): print ("WARNING csend: payload size == 0... continuing")
        totptbs = int(len(payload) / self.PAYLOAD_SIZE)
        if ((len(payload) % self.PAYLOAD_SIZE)!=0): totptbs += 1

        # Initialize stats counters
        FAILED         = 0
        stats_psent    = 0
        stats_retrans  = 0

        # RTT estimators
        timeout_time   =  1    # 1 second
        estimated_rtt  = -1
        dev_rtt        =  1

        # the_sock.settimeout(5)      # 5 seconds initial timeout... LoRa is slow
        r = seriallopy.writeread(b"settimeout"+bytes(struct.pack("f", 5) ))
        if self.HARD_DEBUG_MODE: print("LORACTP157 received: ", r)

        # stop and wait
        seqnum = self.ZERO
        acknum = self.ONE
        for cp in range(totptbs):

            last_pkt = True if (cp == (totptbs-1)) else False

            # Getting a block of max self.PAYLOAD_SIZE from "payload"
            blocktbs = payload[0:self.PAYLOAD_SIZE]  # Taking self.PAYLOAD_SIZE bytes ToBeSent
            payload  = payload[self.PAYLOAD_SIZE:]   # Shifting the input string

            packet = self.__make_packet(sndr_addr, rcvr_addr, seqnum, acknum, self.ITS_DATA_PACKET, last_pkt, blocktbs)
            if self.DEBUG_MODE: self.__debug_printpacket("150: sending packet", packet)

            # trying 3 times
            keep_trying = 3
            while (keep_trying > 0):

                send_time = time.time()
                ack = seriallopy.writeread(b"SR"+packet)
                recv_time = time.time()
                if self.DEBUG_MODE: print("DEBUG 163: received ack", ack)

                if ack != b"socket.timeout":
                    # self.__unpack packet information
                    ack_saddr, ack_daddr, ack_seqnum, ack_acknum, ack_is_ack, ack_final, ack_check, ack_content = self.__unpack(ack)
                    if (rcvr_addr == self.ANY_ADDR) or (rcvr_addr == b''):
                        rcvr_addr = ack_saddr       # in case rcvr_addr was self.ANY_ADDR and payload needs many packets

                    # Check if valid...
                    if (ack_is_ack) and (ack_acknum == seqnum) and (sndr_addr == ack_daddr) and (rcvr_addr == ack_saddr):
                        stats_psent   += 1
                        # No more need to retry
                        break
                    else:
                        # Received packet not valid
                        if self.DEBUG_MODE: print ("ERROR: ACK received not valid")

                if self.DEBUG_MODE: self.__debug_printpacket("re-sending packet", packet)
                if self.DEBUG_MODE: print ("DEBUG 183: attempt number: ", keep_trying)
                stats_psent   += 1
                stats_retrans += 1
                keep_trying   -= 1
                if(keep_trying == 0):
                    FAILED = -1
                    break

            # Check if last packet or failed to send a packet...
            if last_pkt or (FAILED<0): break

            # RTT calculations
            sample_rtt = recv_time - send_time
            if estimated_rtt == -1:
                estimated_rtt = sample_rtt
            else:
                estimated_rtt = estimated_rtt * 0.875 + sample_rtt * 0.125
            dev_rtt = 0.75 * dev_rtt + 0.25 * abs(sample_rtt - estimated_rtt)
            # the_sock.settimeout(estimated_rtt + 4 * dev_rtt)
            r = seriallopy.writeread(b"settimeout"+bytes(struct.pack("f", estimated_rtt + 4 * dev_rtt)) )
            print("settimeout received: ", r)

            if self.DEBUG_MODE: print ("202: setting timeout to", estimated_rtt + 4 * dev_rtt)

            # Increment sequence and ack numbers
            seqnum = (seqnum + self.ONE) % 2    # self.ONE if seqnum == self.ZERO else self.ZERO
            acknum = (acknum + self.ONE) % 2    # self.ONE if acknum == self.ZERO else self.ZERO

        if self.DEBUG_MODE: print ("DEBUG 208: RETURNING tsend")
        return rcvr_addr, stats_psent, stats_retrans, FAILED




    def _crecv(self, my_addr, snd_addr):

        # Shortening addresses to last 8 bytes
        my_addr  = my_addr[8:]
        snd_addr = snd_addr[8:]
        if self.DEBUG_MODE: print ("DEBUG 247: my_addr, snd_addr: ", my_addr, snd_addr)

        # Buffer storing the received data to be returned
        rcvd_data = b''

        next_acknum = self.ONE
        # the_sock.settimeout(5)      # 5 seconds initial timeout... LoRa is slow
        r = seriallopy.writeread(b"settimeout"+bytes(struct.pack("f", 5) ))
        if self.HARD_DEBUG_MODE: print("LORACTP242 received: ", r)

        if (snd_addr == self.ANY_ADDR) or (snd_addr == b''): SENDER_ADDR_KNOWN = False
        while True:
            try:
                packet = seriallopy.writeread(b"R")
                if self.DEBUG_MODE: print ("DEBUG 248: packet received: ", packet)

                if packet != b"socket.timeout":

                    inp_src_addr, inp_dst_addr, inp_seqnum, inp_acknum, is_ack, last_pkt, check, content = self.__unpack(packet)
                    # getting sender address, if unknown, with the first packet
                    if (not SENDER_ADDR_KNOWN):
                        snd_addr = inp_src_addr
                        SENDER_ID_KNOWN = True
                    # Checking if a "valid" packet... i.e., either for me or broadcast
                    if (inp_dst_addr != my_addr) and (inp_dst_addr != self.ANY_ADDR):
                        if self.DEBUG_MODE: print("DISCARDED received packet not for me!!")
                        continue
                else:
                    # got a timeout
                    if self.DEBUG_MODE: print ("EXCEPTION!! Socket timeout: ", time.time())
                    continue
            except Exception as e:
                print ("EXCEPTION!! Packet not valid: ", e)
                continue

            if self.DEBUG_MODE: print("DEBUG 244: get_checksum(content)", self.__get_checksum(content))
            checksum_OK = (check == self.__get_checksum(content))
            if (checksum_OK) and (next_acknum == inp_acknum) and (snd_addr == inp_src_addr):
                rcvd_data += content

                # Sending ACK
                next_acknum = (inp_acknum + self.ONE) % 2
                ack_segment = self.__make_packet(my_addr, inp_src_addr, inp_seqnum, next_acknum, self.ITS_ACK_PACKET, last_pkt, b'')
                r = seriallopy.writeread(b"S"+ack_segment)
                if self.DEBUG_MODE: print("DEBUG 252: Sent ACK", ack_segment)
                if (last_pkt):
                    break
            else:
                if self.DEBUG_MODE: print ("DEBUG 257: packet not valid", packet)

        return rcvd_data, snd_addr


    def connect(self, dest=ANY_ADDR):
        print("loractp: connecting to... ", dest)
        rcvr_addr, stats_psent, stats_retrans, FAILED = self._csend(b"CONNECT", self.lora_mac, dest)
        return self.my_addr, rcvr_addr, stats_retrans, FAILED


    def listen(self, sender=ANY_ADDR):
        print("loractp: listening for...", sender)
        rcvd_data, snd_addr = self._crecv(self.lora_mac, sender)
        print(rcvd_data)
        if (rcvd_data==b"CONNECT"):
            return self.my_addr, snd_addr, 0
        else:
            return self.my_addr, snd_addr, -1

    def sendit(self, addr=ANY_ADDR, payload=b''):
        rcvr_addr, stats_psent, stats_retrans, FAILED = self._csend(payload, self.lora_mac, addr)
        return rcvr_addr, stats_retrans, FAILED

    def recvit(self, addr=ANY_ADDR):
        rcvd_data, snd_addr = self._crecv(self.lora_mac, addr)
        return rcvd_data, snd_addr
