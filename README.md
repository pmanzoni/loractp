# loractp
LoRaCTP: LoRa content transfer protocol

The code in this repository allows to tranfer blocks of bytes ("content") over a LoRa (pure LoRa, no LoRaWAN) channel.

It is written in micropython and tested on a [LoPy4](https://pycom.io/product/lopy4/).

File `loractp.py` includes the class definition.

File `receiver.py` show the example of a receiving node.

File `sender.py` show the example of a sending node. File `sender_loop.py` allows to send content in loop.