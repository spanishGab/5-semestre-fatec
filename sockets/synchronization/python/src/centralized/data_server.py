from constants import GITHUB_DIR, DEFAULT_HOST

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Server import Server

from libraries.constants.constants import STX, ACK, EOT, NAK

import socket

def server():
    while True:
        data_server = Server(host=DEFAULT_HOST, port=5002)
        data_server.connect(listen=2)

        client_request = data_server.receive_message(1)

        if client_request == STX:
            data_server.send_message(ACK)
        else:
            data_server.send_message(NAK)
            data_server.log_message("Could not receive message from client, aborting!")
            return None

        client_message = data_server.receive_message(1024)

        data_server.send_message(EOT)
        
        print(client_message.decode())
        
        data_server.connection.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
    server()