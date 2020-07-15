#!/usr/bin/python3
from common import *
import time, argparse


def main(message):

    start_transmission = False
    # Tell peer that transmission will start
    while not start_transmission:
        s=connect_onos('127.0.0.1', 6633, 0xEF)
        time.sleep(0.1)
        # sending a ECHO_REQUEST to check if the OF connection is still alive
        echo_req_pkt = OFPTEchoRequest(xid=100)
        s.send(bytes(echo_req_pkt))
        time.sleep(0.01)
        # check if a ECHO_REPLY has been received, if not, transmission has begun
        pkts = dissect(s.recv(4096))
        if len(pkts) > 0:
            for packet in pkts:
                if packet.type == 3:
                    print('Sending SoT')
                    time.sleep(5)
                    s.close()
                    start_transmission = True
        else:
            s.close()

    # Transmit message
    for i in range(len(message)):
        print('Sending ' + message[i])

        # encoding the character in ASCII hex
        char_hex = message[i].encode()
        first_hex = int(hex(char_hex[0])[2:3], 16)
        second_hex = int(hex(char_hex[0])[3:4], 16)

        # sending first hex
        print('sending ' + str(first_hex))
        s = connect_onos('127.0.0.1', 6633, first_hex)
        time.sleep(3.6)
        s.close()

        # sending second hex
        print('sending ' + str(second_hex))
        s = connect_onos('127.0.0.1', 6633, second_hex)
        time.sleep(3.6)
        s.close()

    end_transmission = False
    # Tell peer that transmission is done
    while not end_transmission:
        s=connect_onos('127.0.0.1', 6633, 0xFF)
        time.sleep(0.1)
        # sending a ECHO_REQUEST to check if the OF connection is still alive
        echo_req_pkt = OFPTEchoRequest(xid=100)
        s.send(bytes(echo_req_pkt))
        time.sleep(0.01)
        # check if a ECHO_REPLY has been received, if not, transmission has begun
        pkts = dissect(s.recv(4096))
        if len(pkts) > 0:
            for packet in pkts:
                if packet.type == 3:
                    print('Sending EoT')
                    time.sleep(5)
                    s.close()
                    end_transmission = True
        else:
            s.close()

    print(f'message "{message}" sent')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", help="Message that will be sent to the receiver...",
                        type=str, required=True)
    args = parser.parse_args()

    while True : main(args.message)
