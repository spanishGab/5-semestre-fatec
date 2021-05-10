from zmq import REQ
import sys
from constants import (GITHUB_DIR, MESSAGE_SENT_TEXT, MESSENGER_SERVER_PORT)

sys.path.insert(1, GITHUB_DIR)

from libraries.messengers.BaseZeroMqSocketContextManager import \
    BaseZeroMqSocketContextManager

from concurrent.futures import ThreadPoolExecutor

CLIENT_A_NAME = "Gabriel"


def send_message():
    client_a = BaseZeroMqSocketContextManager(init_context=True)

    client_a.add_socket_to_context(socket_name=CLIENT_A_NAME, socket_type=REQ)
    
    client_a.connect_socket_to_address(CLIENT_A_NAME, 
                                       address_port=MESSENGER_SERVER_PORT)
    
    while True:
        message = input(f"{CLIENT_A_NAME}, Type your message: ").encode()

        client_a.send_message(CLIENT_A_NAME, message)

        message = client_a.receive_message(CLIENT_A_NAME)

        print(MESSAGE_SENT_TEXT.format(cli=message[0].decode(), msg=message[1].decode()))
        

    client_a.disconnect_socket_from_address(CLIENT_A_NAME)


if __name__ == '__main__':
    send_message()
