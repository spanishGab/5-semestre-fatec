from constants import GITHUB_DIR, DEFAULT_HOST

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Server import Server

from libraries.constants.constants import STX, ACK, EOT, NAK

import socket

import time

from  concurrent.futures import ThreadPoolExecutor

FOO_CLIENT_PORT = 5002
BAR_CLIENT_PORT = 5003

clients_message = ["Clients message",]

def server(port: int):
    global clients_message

    while True:
        try:
            data_server = Server(host=DEFAULT_HOST, port=port)
            data_server.connect()

            client_request = data_server.receive_message(1)

            if client_request == STX:
                data_server.send_message(ACK)
            else:
                data_server.send_message(NAK)
                data_server.log_message("Could not receive message from client, aborting!")
                return None

            client_message = data_server.receive_message(1024)

            time.sleep(5)

            data_server.send_message(EOT)
            
            print(client_message.decode())

            clients_message.append(client_message.decode())

        except Exception as e:
            data_server.shutdown_connection()
            raise e
        finally:
            data_server.shutdown_connection()
        

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(server, FOO_CLIENT_PORT)
        executor.submit(server, BAR_CLIENT_PORT)
    
    print(' : '.join(clients_message))