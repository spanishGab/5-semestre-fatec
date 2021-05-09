import sys
import socket
from constants import (GITHUB_DIR, NETWORK_INTERFACE, INTERFACE_MAC_ADDRESS,
                       ETHERNET_FRAME_TYPE)

sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.EthernetSocket import EthernetSocket

message = INTERFACE_MAC_ADDRESS*2 + ETHERNET_FRAME_TYPE + 'Hi'.encode()

tx = EthernetSocket(alias='TX', interface=NETWORK_INTERFACE)
tx.connect()
tx.send_mesage(message)
tx.close_connection()
