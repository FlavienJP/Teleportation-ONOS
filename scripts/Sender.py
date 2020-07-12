from .common import *
import time, argparse


def main(message):

    # Tell peer Start_of_transmission
    s=connect_onos('127.0.0.1', 6633, 0xEF)
    time.sleep(5)
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
        time.sleep(2.125)
        s.close()

        # sending second hex
        print('sending ' + str(second_hex))
        s = connect_onos('127.0.0.1', 6633, second_hex)
        time.sleep(2.225)
        s.close()

        # sending EndOfTransmission
        s = connect_onos('127.0.0.1', 6633, 0xFF)
        time.sleep(5)
        s.close()

        print('message sent')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", help="Message that will be sent to the receiver...",
                        type=str, required=True)
    args = parser.parse_args()

    main(args.message)

