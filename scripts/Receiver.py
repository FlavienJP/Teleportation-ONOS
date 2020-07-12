from .common import *
import time


def main():

    # Wait for start of transmission
    s=connect_onos('127.0.0.1', 6633, 0xEF)
    time.sleep(5)
    s.close()

    while True:
        # Check if connection still alive
        echo_req_pkt = OFPTEchoRequest(xid=100)
        s.send(bytes(echo_req_pkt))
        pkts = dissect(s.recv(4096))
        echo_rep_pkt = OFPTEchoReply(xid=[pkt.xid for pkt in pkts if pkt.type == 3][0])
        s.send(bytes(echo_req_pkt))
        time.sleep(0.025)

if __name__ == "__main__":
    main()
