# Reproduction d'une attaque par téléportation sur un controleur ONOS

_Article MISC n° 114_

_Flavien Joly-Pottuz / Stefano Secci_ | _**CNAM PARIS**_


## Sender.py
```
root@misc:~# ./Sender.py -h
usage: Sender.py [-h] [--controller CONTROLLER] [--port PORT] --message
                 MESSAGE

optional arguments:
  -h, --help            show this help message and exit
  --controller CONTROLLER
                        IPv4 address used by the remote controller, localhost
                        by default.
  --port PORT           Port used by the remote controller, 6633 by default.
  --message MESSAGE     Message that will be sent to the receiver.
```

## Receiver.py
```
root@misc:~# ./Receiver.py -h
usage: Receiver.py [-h] [--controller CONTROLLER] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --controller CONTROLLER
                        IPv4 address used by the remote controller, localhost
                        by default.
  --port PORT           Port used by the remote controller, 6633 by default.

```
