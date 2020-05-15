# LoRaCTP: LoRa Content Transfer Protocol


The code in this repository allows to transfer blocks of bytes ("content") over a LoRa (pure LoRa, no LoRaWAN) channel. The library was tested with content of the size of up to 100kB.

It is based on a stop & wait protocol, inspired by https://github.com/arturenault/reliable-transport-protocol by Artur Upton Renault.


## Folder `loractp`

The code in this folder is written in MicroPython and tested on a [LoPy4](https://pycom.io/product/lopy4/) quadruple bearer MicroPython enabled development board. 

File `loractp.py` includes the class definition. File `boot.py` simply disables the WiFi to limit interferences.

* Files `ping.py` and `pong.py` are examples of a request/response interaction

* File `receiver.py` shows the example of a receiving node.

* File `sender.py` shows the example of a sending node, while  `sender_loop.py` allows to send content in loop.


## Folder `lopyserialproxy`

The code in this folder offers the same functionalities of `loractp.py`  but to be used by a generic python3 capable device (we tested it with a Raspberry Pi 3 Model B+) using the LoPy4 (connected via USB) only as a LoRa adaptor.
Code in subfolder `lopy4code` must be loaded in a LoPy and it starts immediately when the device is powered (ready after a 3 seconds red led blink followed by a green blink).
Code in subfolder `p3code` is basically the rewriting of the code in the main repository (Folder `loractp`). 

* subfolder `lsp` containes:
- file  `loractp.py` the generic python3 version
- file `seriallopy.py` the code to interface with the LoPy via serial channel.

* File `ping.py` can be tested with the `loractp/pong.py` file and is an example of a request/response interaction.

* File `rndsender.py` shows the example of a sender randomly sending messages in broadcast. 

