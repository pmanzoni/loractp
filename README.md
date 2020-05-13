# LoRaCTP: LoRa Content Transfer Protocol

The code in this repository allows to transfer blocks of bytes ("content") over a LoRa (pure LoRa, no LoRaWAN) channel.

It is based on a stop & wait protocol and adapted to a LoRa raw channel (inspired by https://github.com/arturenault/reliable-transport-protocol by Artur Upton Renault).

It is written in MicroPython and tested on a [LoPy4](https://pycom.io/product/lopy4/) quadruple bearer MicroPython enabled development board.


* File `loractp.py` includes the class definition.

* File `receiver.py` shows the example of a receiving node.

* File `sender.py` shows the example of a sending node, while  `sender_loop.py` allows to send content in loop.


## Folder `lopyserialproxy`

The code in this folder offers the same functionalities of `loractp.py`  but to be used by a generic python3 capable device (we tested it with a Raspberry Pi 3B) using a LoPy4 (connected via USB) used as a LoRa adaptor.
Code in subfolder `lopy4code` must be loaded in a LoPy and it start immediately when the device is powered (a 3 second red led blink followed by a green blink)
Code in subfolder `p3code` is basically the rewriting of the code in the main repository but it is supposed to be executed in a "generic python3 capable device"... for example a Raspberry Pi. As before:

* File `loractp.py` includes the class definition.

* File `receiver.py` shows the example of a receiving node.

* File `sender.py` shows the example of a sending node, while  `sender_loop.py` allows to send content in loop.

