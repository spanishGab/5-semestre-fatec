from constants import *

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Client import Client
from libraries.sockets.Server import Server

from libraries.constants.constants import STX, ACK, NAK, CAN, EOT

from concurrent.futures import ThreadPoolExecutor

from threading import Semaphore

import time

SERVER_PORT = 5000
FOO_CLIENT_PORT = 6000
FOO_SERVER_PORT = 6001

SEMAPHORE = Semaphore(1)

not_using_server = False


def receive_client_access_request():
    global not_using_server

    try:
        foo_server = Server('foo_partner', DEFAULT_HOST, FOO_SERVER_PORT)
        foo_server.connect()
        foo_server.log_mesage("Connected foo server")

        foo_server.log_mesage("Waiting for a NAK byte from partner")
        access_request = foo_server.receive_mesage(1)

        # time.sleep(0.2)

        while True:
            if access_request == NAK:
                foo_server.log_mesage("NAK byte received")
                foo_server.log_mesage("Partner requsted for server access")

                with SEMAPHORE:
                    if not_using_server:
                        foo_server.log_mesage("Permission granted")

                        foo_server.log_mesage("Sending an ACK byte to partner")
                        foo_server.send_mesage(ACK)
                        return None
                    else:
                        foo_server.log_mesage("Permission denied")

                        foo_server.log_mesage("Sending an CAN byte to partner")
                        foo_server.send_mesage(CAN)

                        foo_server.log_mesage("Waiting for a NAK byte from partner")
                        access_request = foo_server.receive_mesage(1)
            else:
                foo_server.log_mesage(access_request+" byte received, aborting")
                return None
    except Exception as e:
        foo_server.shutdown_connection()
        foo_server.close_connection()
        raise e
    finally:
        foo_server.shutdown_connection()
        foo_server.close_connection()


def send_client_mesage(mesage: bytes, server_port: int):
    global not_using_server

    try:
        foo_client = Client('foo_partner', DEFAULT_HOST, FOO_CLIENT_PORT)
        try_client_connection(foo_client)
        foo_client.log_mesage("Connected foo client")

        foo_client.log_mesage("Sending a NAK byte to partner")
        foo_client.send_mesage(NAK)

        foo_client.log_mesage("Waiting for an ACK byte from partner")
        partner_response = foo_client.receive_mesage(1)

        while True:
            if partner_response == ACK:
                with SEMAPHORE:
                    not_using_server = False

                foo_client.log_mesage("ACK byte received")
                foo_client.log_mesage("Starting transference")
                
                server_client = Client('foo_client', DEFAULT_HOST, server_port)
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
                foo_client.log_mesage("CAN byte received")
                foo_client.log_mesage("Permission denied")

                foo_client.log_mesage("Sending a NAK byte to partner")
                foo_client.send_mesage(NAK)

                foo_client.log_mesage("Waiting for an ACK byte from partner")
                partner_response = foo_client.receive_mesage(1)

                time.sleep(3)
                continue
            else:
                foo_client.log_mesage(partner_response+" byte received, aborting")
                return None
    except Exception as e:
        foo_client.shutdown_connection()
        server_client.shutdown_connection()
        foo_client.close_connection()
        server_client.close_connection()
        raise e
    finally:
        foo_client.shutdown_connection()
        foo_client.close_connection()


def try_client_connection(client: Client):
    while True:
        try:
            client.connect()
            break
        except ConnectionRefusedError:
            continue


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(send_client_mesage, b'I am foo', SERVER_PORT)
            
        executor.submit(receive_client_access_request)
        
