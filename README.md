# LoRaCTP: LoRa Content Transfer Protocol

The code in this repository allows to transfer blocks of bytes ("content") over a LoRa (pure LoRa, no LoRaWAN) channel.

It is based on stop & wait like protocol and adapted to a LoRa raw channel (inspired by https://github.com/arturenault/reliable-transport-protocol by Artur Upton Renault).

It is written in MicroPython and tested on a [LoPy4](https://pycom.io/product/lopy4/) quadruple bearer MicroPython enabled development board.


File `loractp.py` includes the class definition.

File `receiver.py` shows the example of a receiving node.

File `sender.py` shows the example of a sending node. File `sender_loop.py` allows to send content in loop.
