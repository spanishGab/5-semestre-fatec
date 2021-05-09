import socket
from constants import (GITHUB_DIR, NETWORK_INTERFACE, INTERFACE_MAC_ADDRESS,
                       ETHERNET_FRAME_TYPE)
import sys

sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.EthernetSocket import EthernetSocket


ETH_FRAME_LEN = 1514
FRAME_HEADER_LENGTH = 14

rx = EthernetSocket(alias='RX', interface=NETWORK_INTERFACE)
rx.connect()

message_frame = rx.receive_mesage(ETH_FRAME_LEN)
data = message_frame[FRAME_HEADER_LENGTH:].decode()
print(data)
rx.close_connection()