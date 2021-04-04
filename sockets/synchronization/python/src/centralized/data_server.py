from constants import GITHUB_DIR, DEFAULT_HOST

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Server import Server

from libraries.constants.constants import STX, ACK, EOT, NAK

import socket

import time

from  concurrent.futures import ThreadPoolExecutor

FOO_CLIENT_PORT = 6000
BAR_CLIENT_PORT = 6001
TMP_CLIENT_PORT = 6002

clients_message = ["Clients mesage",]

def server(port: int):
    global clients_message

    data_server = Server(alias='data_server', host=DEFAULT_HOST, port=port)
    data_server.connect()
    data_server.log_mesage("Connected to port "+str(port))
    try:
        while True:
            data_server.log_mesage("Waiting for a STX byte")
            client_request = data_server.receive_mesage(1)

            if client_request == STX:
                data_server.log_mesage("STX byte received")
                data_server.log_mesage("Sending ACK byte to start transference")
                data_server.send_mesage(ACK)
            else:
                data_server.send_mesage(NAK)
                data_server.log_mesage("Could not receive mesage from client, aborting!")
                break

            data_server.log_mesage("Receiving client mesage")
            client_message = data_server.receive_mesage(1024)

            data_server.log_mesage("Mesage received")

            data_server.log_mesage("Logging client message 7 times")
            cont = 1
            while cont <= 7:
                print(client_message.decode())
                time.sleep(1)
                cont += 1

            clients_message.append(client_message.decode())
            
            data_server.log_mesage("Sending EOT byte to confirm transference")
            data_server.send_mesage(EOT)

    except Exception as e:
        data_server.shutdown_connection()
        raise e
    finally:
        data_server.shutdown_connection()
        

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(server, FOO_CLIENT_PORT)
        executor.submit(server, BAR_CLIENT_PORT)
        executor.submit(server, TMP_CLIENT_PORT)
    
    print(' : '.join(clients_message))