from constants import *

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Client import Client
from libraries.sockets.Server import Server

from libraries.constants.constants import STX, ACK, NAK, CAN, EOT

from concurrent.futures import ThreadPoolExecutor

from threading import Semaphore

import time

SERVER_PORT = 5001
BAR_SERVER_PORT = 6000
BAR_CLIENT_PORT = 6001

SEMAPHORE = Semaphore(1)

not_using_server = True
import time

def receive_client_message():
    global not_using_server

    try:
        bar_server = Server('bar_partner', DEFAULT_HOST, BAR_SERVER_PORT)
        bar_server.connect()
        bar_server.log_mesage("Connected bar partner")

        bar_server.log_mesage("Waiting for a NAK byte from partner")
        access_request = bar_server.receive_mesage(1)

        # time.sleep(0.2)

        while True:
            if access_request == NAK:
                bar_server.log_mesage("NAK byte received")
                bar_server.log_mesage("Partner requsted for server access")

                with SEMAPHORE:
                    if not_using_server:
                        bar_server.log_mesage("Permission granted")

                        bar_server.log_mesage("Sending an ACK byte to partner")
                        bar_server.send_mesage(ACK)
                        return None
                    else:
                        bar_server.log_mesage("Permission denied")

                        bar_server.log_mesage("Sending an CAN byte to partner")
                        bar_server.send_mesage(CAN)

                        bar_server.log_mesage("Waiting for a NAK byte from partner")
                        access_request = bar_server.receive_mesage(1)
            else:
                bar_server.log_mesage(access_request+" byte received, aborting")
                return None
    except Exception as e:
        bar_server.shutdown_connection()
        raise e
    finally:
        bar_server.shutdown_connection()


def send_client_mesage(mesage: bytes, server_port: int):
    global not_using_server

    try:
        bar_client = Client('bar_partner', DEFAULT_HOST, BAR_CLIENT_PORT)
        try_client_connection(bar_client)
        bar_client.log_mesage("Connected bar partner")

        bar_client.log_mesage("Sending a NAK byte to partner")
        bar_client.send_mesage(NAK)

        bar_client.log_mesage("Waiting for an ACK byte from partner")
        partner_response = bar_client.receive_mesage(1)

        while True:
            if partner_response == ACK:
                with SEMAPHORE:
                    not_using_server = False

                bar_client.log_mesage("ACK byte received")
                bar_client.log_mesage("Starting transference")
                
                server_client = Client('bar_client', DEFAULT_HOST, server_port)
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

                        server_client.log_mesage("EOT byte received")
                        server_client.log_mesage("Trensfrece successfully finished")
                        server_client.shutdown_connection()
                        
                        with SEMAPHORE:
                            not_using_server = True
                        
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
                bar_client.log_mesage("CAN byte received")
                bar_client.log_mesage("Permission denied")

                bar_client.log_mesage("Sending a NAK byte to partner")
                bar_client.send_mesage(NAK)

                bar_client.log_mesage("Waiting for an ACK byte from partner")
                partner_response = bar_client.receive_mesage(1)

                time.sleep(3)
                continue
            else:
                bar_client.log_mesage(partner_response+" byte received, aborting")
                return None
    except Exception as e:
        bar_client.shutdown_connection()
        server_client.shutdown_connection()
        raise e
    finally:
        bar_client.shutdown_connection()


def try_client_connection(client: Client):
    while True:
        try:
            client.connect()
            break
        except ConnectionRefusedError:
            continue


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(send_client_mesage, b'I am bar', SERVER_PORT)

        executor.submit(receive_client_message)

