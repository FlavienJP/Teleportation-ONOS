#!/usr/bin/python3
from common import *
import time, argparse


controller_ip = 'onos'
openflow_port = 6633

def main(message):

    start_transmission = False
    # Tell peer that transmission will start
    while not start_transmission:
        start_time = time.time()
        s=connect_onos(controller_ip, openflow_port, 0xEF)
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
        print('time used: ', time.time() - start_time)

    # Transmit message
    for i in range(len(message)):
        start_time = time.time()
        print('Sending ' + message[i])

        # encoding the character in ASCII hex
        char_hex = message[i].encode()
        first_hex = int(hex(char_hex[0])[2:3], 16)
        second_hex = int(hex(char_hex[0])[3:4], 16)

        # sending first hex
        print('sending ' + str(first_hex))
        s = connect_onos(controller_ip, openflow_port, first_hex)
        time.sleep(3.72)
        s.close()
        print('time used: ', time.time() - start_time)
        start_time = time.time()

        # sending second hex
        print('sending ' + str(second_hex))
        s = connect_onos(controller_ip, openflow_port, second_hex)
        time.sleep(3.72)
        s.close()
        print('time used: ', time.time() - start_time)

    end_transmission = False
    # Tell peer that transmission is done
    while not end_transmission:
        start_time = time.time()
        s=connect_onos(controller_ip, openflow_port, 0xFF)
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
                    time.sleep(10)
                    s.close()
                    end_transmission = True
                    break
        else:
            s.close()
        print('time used: ', time.time() - start_time)
    print(f'message "{message}" sent')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", help="Message that will be sent to the receiver...",
                        type=str, required=True)
    args = parser.parse_args()

    while True : main(args.message)
