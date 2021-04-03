from constants import (
    GITHUB_DIR, 
    DEFAULT_HOST, 
    FOO_MESAGE, 
    BAR_MESAGE
)

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Client import Client

from libraries.constants.constants import ACK, NAK, CAN, STX, EOT

from threading import Thread


CONTROLLER_PORT = 5001
SERVER_PORT = 5003


def client_mesage(controller_port: int, client: Client, mesage: bytes):
    controller_cli = Client(host=DEFAULT_HOST, port=controller_port)
    
    controller_cli.log_message("Connecting to the controller")
    
    controller_cli.connect()

    controller_cli.log_message("Connected successfully")

    controller_cli.log_message("Sending an NAK byte to the controller "+
        "(acquire request)")
    controller_cli.send_message(NAK)

    controller_cli.log_message("Waiting for an ACK byte from the controller")
    response = controller_cli.receive_message(1)
    
    while True:
        if response == ACK:
            controller_cli.log_message("ACK byte received, permission granted")
            controller_cli.log_message("Starting transference")

            client.log_message("Sending a STX byte to the server")
            client.send_message(STX)

            client.log_message("Waiting for an ACK byte")
            server_response = client.receive_message(1)

            if server_response == ACK:
                controller_cli.log_message("ACK byte received")
                controller_cli.log_message("Sending thee mesage to the server")

                client.send_message(mesage)
                
                client.log_message("Waiting for an EOT byte")
                server_response = client.receive_message(1)
            else:
                client.log_message("Transference not accepted by server, aborting!")
                return None
            
            if server_response == EOT:
                controller_cli.log_message("EOT byte received")
                client.log_message("Transference successfully finished")
                break

        elif response == CAN:
            controller_cli.log_message("Server in use, please wait!")
        else:
            controller_cli.log_message("Error! Response received: "+response.decode())
            return None
    
    controller_cli.log_message("Sending an NAK byte to the controller "+
        "(release request)")
    controller_cli.send_message(NAK)

    controller_cli.log_message("Waiting for an ACK byte from the controller")
    response = controller_cli.receive_message(1)

    if response == ACK:
        controller_cli.log_message("ACK byte received")
        controller_cli.log_message("Released server")
    elif response == CAN:
        raise Exception("Requested a 'release' before an 'acquire'"+
            ", aborting!")
    else:
        return None

if __name__ == '__main__':
    client_bar = Client(host=DEFAULT_HOST, port=SERVER_PORT)
    client_bar.connect()

    try:
        client_mesage(CONTROLLER_PORT, client_bar, b'I am bar')
    except Exception as e:
        client_bar.shutdown_connection()
        raise e
    finally:
        client_bar.shutdown_connection()

    
    
