from constants import GITHUB_DIR, DEFAULT_HOST

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Server import Server

import socket

if __name__ == '__main__':
    data_server = Server(host=DEFAULT_HOST, port=5001)
    data_server.connect(listen=2)

    print(data_server.receive_message(1024))
    data_server.connection.shutdown(socket.SHUT_RDWR)
