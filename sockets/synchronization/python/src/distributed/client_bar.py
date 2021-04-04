from constants import *

from PartnerClient import PartnerClient

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Client import Client
from libraries.sockets.Server import Server

# from partner_job import send_client_mesage, receive_client_message, try_client_connection

from concurrent.futures import ThreadPoolExecutor

from threading import Semaphore

SERVER_PORT = 5001
BAR_SERVER_PORT = 6000
BAR_CLIENT_PORT = 6001

SEMAPHORE = Semaphore(1)

partner = PartnerClient()

def receive_client_message(conn: Server):
    global partner

    # try:
    conn.log_mesage("Receiving NAK byte from partner client")
    access_request = conn.receive_mesage(1)

    if access_request == NAK:
        conn.log_mesage("NAK byte received")
        conn.log_mesage("Partner requsted for server access")

        with SEMAPHORE:
            accssses_granted = partner.can_access_server()

        if accssses_granted:
            conn.log_mesage("Permission granted")

            conn.log_mesage("Sending an ACK byte to partner")
            conn.send_mesage(ACK)
        else:
            conn.log_mesage("Permission denied")

            conn.log_mesage("Sending an CAN byte to partner")
            conn.send_mesage(CAN)
    else:
        conn.log_mesage(access_request+" byte received, aborting")
        return None
    # except Exception as e:
    #     conn.shutdown_connection()
    #     raise e
    # finally:
    #     conn.shutdown_connection()


def send_client_mesage(mesage: bytes, 
                       conn: Client, 
                       server_port: int):
    global partner

    # try:
    conn.log_mesage("Sending a NAK byte to partner client")
    conn.send_mesage(NAK)

    conn.log_mesage("Receiving ACK byte from partner client")
    partner_response = conn.receive_mesage(1)

    while True:
        if partner_response == ACK:
            with SEMAPHORE:
                partner.not_using_server = False

            conn.log_mesage("ACK byte received")
            conn.log_mesage("Starting transference")
            
            server_client = Client(DEFAULT_HOST, server_port)
            server_client.connect()

            server_client.log_mesage("Connected to server")
            server_client.log_mesage("Sending an STX byte to server")
            server_client.send_mesage(STX)

            server_client.log_mesage("Waiting for a ACK byte from server")
            server_response = server_client.receive_mesage(1)

            if server_response == ACK:
                server_client.log_mesage("ACK byte received")
                server_client.log_mesage("Sending mesage to the server")
                server_client.send_mesage(mesage)

                server_client.log_mesage("Waiting for a EOT byte from server")
                server_response = server_client.receive_mesage(1)

                if server_response == EOT:
                    with SEMAPHORE:
                        partner.not_using_server = True

                    server_client.log_mesage("EOT byte received")
                    server_client.log_mesage("Trensfrece successfully finished")
                    server_client.shutdown_connection()
                    return None
                else:
                    server_client.log_mesage(server_response+" byte received, "+
                        "aborting")
                    return None
            else:
                server_client.log_mesage(server_response+" byte received, "+
                        "aborting")
                return None

        elif partner_response == CAN:
            conn.log_mesage("CAN byte received")
            conn.log_mesage("Permission denied")

            conn.log_mesage("Waiting for an ACK byte")
            partner_response = conn.receive_mesage(1)
            continue
        else:
            conn.log_mesage(partner_response+" byte received, aborting")
            return None
    # except Exception as e:
    #     conn.shutdown_connection()
    #     server_client.shutdown_connection()
    #     raise e
    # finally:
    #     conn.shutdown_connection()


def try_client_connection(client: Client):
    while True:
        try:
            client.connect()
            break
        except ConnectionRefusedError:
            continue


if __name__ == '__main__':

    bar_client = Client(DEFAULT_HOST, BAR_CLIENT_PORT)
    try_client_connection(bar_client)
    bar_client.log_mesage("Connected bar client")

    bar_server = Server(DEFAULT_HOST, BAR_SERVER_PORT)
    bar_server.connect()
    bar_server.log_mesage("Connected bar server")

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(send_client_mesage, b'I am bar', 
            bar_client, SERVER_PORT)
        
        executor.submit(receive_client_message, bar_server)