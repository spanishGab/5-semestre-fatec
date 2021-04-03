from constants import GITHUB_DIR, DEFAULT_HOST, FOO_MESAGE, BAR_MESAGE

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Client import Client

from libraries.constants.constants import ACK, NAK, CAN


if __name__ == '__main__':
    controller_cli = Client(host=DEFAULT_HOST, port=5000)
    controller_cli.connect()

    controller_cli.send_message(NAK)

    response = controller_cli.receive_message(1)
    
    if response == ACK:
        client_foo = Client(host=DEFAULT_HOST, port=5001)
        client_foo.connect()

        client_foo.send_message(FOO_MESAGE)

    elif response == CAN:
        controller_cli.log_message("Server in use, please wait")
    
    
    controller_cli.send_message(NAK)

    response = controller_cli.receive_message(1)

    if response == ACK:
        print("Released")
    elif response == CAN:
        raise Exception("Requested a 'release' before an 'acquire'"+
            ", aborting!")


    
    
