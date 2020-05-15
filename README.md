# LoRaCTP: LoRa Content Transfer Protocol


The code in this repository allows to transfer blocks of bytes ("content") over a LoRa (pure LoRa, no LoRaWAN) channel. The library was tested with content of the size of up to 100kB.

It is based on a stop & wait protocol, inspired by https://github.com/arturenault/reliable-transport-protocol by Artur Upton Renault.


## Folder `loractp`

The code in this folder is written in MicroPython and tested on a [LoPy4](https://pycom.io/product/lopy4/) quadruple bearer MicroPython enabled development board. 

File `loractp.py` includes the class definition. File `boot.py` simply disables the WiFi to limit interferences.

* File `pong.py` can be tested with the `lopyserialproxy/p3code/ping.py` file and is an example of a request/response interaction.

* File `plainreceiver.py` shows the example of a receiving node.



## Folder `lopyserialproxy`

The code in this folder offers the same functionalities of `loractp.py`  but to be used by a generic python3 capable device (we tested it with a Raspberry Pi 3 Model B+) using the LoPy4 (connected via USB) only as a LoRa adaptor.
Code in subfolder `lopy4code` must be loaded in a LoPy and it starts immediately when the device is powered (ready after a 3 seconds red led blink followed by a green blink).
Code in subfolder `p3code` is basically the rewriting of the code in the main repository (Folder `loractp`). 

* subfolder `lsp` contains:
	- file  `loractp.py` the generic python3 version
	- file `seriallopy.py` the code to interface with the LoPy via serial channel.

* File `ping.py` can be tested with the `loractp/pong.py` file and is an example of a request/response interaction.

* File `rndsender.py` shows the example of a sender randomly sending messages in broadcast. 

## The ping/pong example.

To execute this example you need to have  a LoPy4 (lopyA)
![](https://i.imgur.com/A0EfDnS.jpg =200x200)

and a Raspberry Pi with a LoPy4 (lopyB) connected via USB
![](https://i.imgur.com/6acWD3b.jpg =200x200).

Copy files `boot.py`, `loractp.py`, and `pong.py` in folder `loractp` in the lopyA, copy all files in `lopyserialproxy/lopy4code` in the lopyB, and copy all files in `lopyserialproxy/p3code` in the Raspberry Pi.

Execute `pong.py` in the lopyA.
The lopyB, if plugged in the Raspberry Pi should be already ready (if you have seen the 3 seconds red led blink followed by a green blink).
Before executing the code in the Raspberry Pi, be sure that the serial port lopyB is connected to is '/dev/ttyACM0'. Otherwise you have to explicitely indicate it in the code when creating the CTPendpoint. Like for example:
````
ctpc = loractp.CTPendpoint(port='/dev/ttyACM1')
````
Now run in the Raspberry Pi shell:
```
$ python3 ping.py
```
You should now see a message going from the Raspberry Pi to the lopyA (ping)... and the response (pong) coming form the lopyA to the Raspberry Pi.

## Caveats
1. Code based on `seriallopy.py` can fail to connect to the UART the first time. It is simply a matter of trying twice

