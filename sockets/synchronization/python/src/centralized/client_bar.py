from constants import (
    GITHUB_DIR, 
    DEFAULT_HOST, 
    BAR_MESAGE
)

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Client import Client

from libraries.constants.constants import ACK, NAK, CAN, STX, EOT

from threading import Thread


CONTROLLER_PORT = 5001
SERVER_PORT = 6001


def client_mesage(mesage: bytes):
    try:
        cli_controller = Client(host=DEFAULT_HOST, port=CONTROLLER_PORT)
        
        cli_controller.log_message("Connecting to the controller")
        
        cli_controller.connect()

        cli_controller.log_message("Connected successfully")

        cli_controller.log_message("Sending an NAK byte to the controller "+
            "(acquire request)")
        cli_controller.send_message(NAK)

        cli_controller.log_message("Waiting for an ACK byte from the controller")
        response = cli_controller.receive_message(1)
        
        while True:
            if response == ACK:
                cli_controller.log_message("ACK byte received, permission granted")

                client_bar = Client(host=DEFAULT_HOST, port=SERVER_PORT)
                client_bar.connect()
                cli_controller.log_message("Connected to server port "+
                    str(SERVER_PORT))

                cli_controller.log_message("Starting transference")
                client_bar.log_message("Sending a STX byte to the server")
                client_bar.send_message(STX)

                client_bar.log_message("Waiting for an ACK byte")
                server_response = client_bar.receive_message(1)

                if server_response == ACK:
                    cli_controller.log_message("ACK byte received")
                    cli_controller.log_message("Sending thee mesage to the server")

                    client_bar.send_message(mesage)
                    
                    client_bar.log_message("Waiting for an EOT byte")
                    server_response = client_bar.receive_message(1)
                else:
                    client_bar.log_message("Transference refused by server, aborting!")
                    return None
                
                if server_response == EOT:
                    cli_controller.log_message("EOT byte received")
                    client_bar.log_message("Transference successfully finished")
                    client_bar.shutdown_connection()
                    break
            else:
                cli_controller.log_message("Error! Response received: "+response.decode())
                return None
        
        cli_controller.log_message("Sending an NAK byte to the controller "+
            "(release request)")
        cli_controller.send_message(NAK)

        cli_controller.log_message("Waiting for an ACK byte from the controller")
        response = cli_controller.receive_message(1)

        if response == ACK:
            cli_controller.log_message("ACK byte received")
            cli_controller.log_message("Released server")
        elif response == CAN:
            raise Exception("Requested a 'release' before an 'acquire'"+
                ", aborting!")
        else:
            return None
    except Exception as e:
        client_bar.shutdown_connection()
        cli_controller.shutdown_connection()
        raise e
    finally:
        cli_controller.shutdown_connection()


if __name__ == '__main__':
    
    client_mesage(b'I am bar')

    
    
