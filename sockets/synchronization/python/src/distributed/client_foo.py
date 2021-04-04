from constants import *

from PartnerClient import PartnerClient

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Client import Client

from libraries.constants.constants import STX, ACK, NAK, CAN , EOT

SERVER_PORT = 5000
PARTNER_CLIENT_PORT = 6001

PARTNER_CONN =  'partner_client_'+str(PARTNER_CLIENT_PORT)

def receive_client_message():
    partner_client = PartnerClient()

    partner_client.add_connection('server', PARTNER_CONN,
        DEFAULT_HOST, PARTNER_CLIENT_PORT)
    partner_client.connections[PARTNER_CONN].log_mesage(
        "Connected to partner client")

    partner_client.connections[PARTNER_CONN].log_mesage("Receiving NAK byte"+
        " from partner client")
    access_request = partner_client.connections[PARTNER_CONN].receive_mesage(1)

    if access_request == NAK:
        partner_client.connections[PARTNER_CONN].log_mesage("NAK byte received")
        partner_client.connections[PARTNER_CONN].log_mesage("Partner requsted"+
            " for server access")
        if partner_client.can_access_server():
            partner_client.connections[PARTNER_CONN].log_mesage("Permission granted")

            partner_client.connections[PARTNER_CONN].log_mesage("Sending an ACK "+
                "byte to partner")
            partner_client.connections[PARTNER_CONN].send_mesage(ACK)
        else:
            partner_client.connections[PARTNER_CONN].log_mesage("Permission denied")

            partner_client.connections[PARTNER_CONN].log_mesage("Sending an CAN "+
                "byte to partner")
            partner_client.connections[PARTNER_CONN].send_mesage(CAN)
    else:
        partner_client.connections[PARTNER_CONN].log_mesage(access_request+
            " byte received, aborting")
        return None


def send_client_mesage(mesage: bytes):
    partner_client = PartnerClient()

    partner_client.add_connection('client', PARTNER_CONN,
        DEFAULT_HOST, PARTNER_CLIENT_PORT)

    partner_client.connections[PARTNER_CONN].log_mesage(
        "Connected to partner client")
    
    partner_client.connections[PARTNER_CONN].log_mesage("Sending a NAK byte"+
        " to partner client")
    partner_client.connections[PARTNER_CONN].send_mesage(NAK)

    partner_client.connections[PARTNER_CONN].log_mesage("Receiving ACK byte"+
        " from partner client")
    partner_response = partner_client.connections[PARTNER_CONN].receive_mesage(1)

    while True:
        if partner_response == ACK:
            partner_client.connections[PARTNER_CONN].log_mesage("ACK byte received")
            partner_client.connections[PARTNER_CONN].log_mesage("Starting "+
                "transference")
            
            server_client = Client(DEFAULT_HOST, SERVER_PORT)
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
                    return None
                else
                    server_client.log_mesage(server_response+" byte received, "+
                        "aborting")
                    return None
            else:
                server_client.log_mesage(server_response+" byte received, "+
                        "aborting")
                return None

        elif partner_response == CAN:
            partner_client.connections[PARTNER_CONN].log_mesage("CAN byte received")
            partner_client.connections[PARTNER_CONN].log_mesage("Permission denied")

            partner_client.connections[PARTNER_CONN].log_mesage("Waiting for an "+
                "ACK byte")
            partner_response = (
                partner_client.connections[PARTNER_CONN].receive_mesage(1))
            continue
        else:
            partner_client.connections[PARTNER_CONN].log_mesage(partner_response+
                " byte received, aborting")
            return None

if __name__ == '__main__'

    

