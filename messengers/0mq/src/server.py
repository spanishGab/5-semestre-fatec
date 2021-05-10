from zmq import REQ
import sys
from constants import (GITHUB_DIR, MESSENGER_SERVER_PORT, MESSAGE_SENT_TEXT)

sys.path.insert(1, GITHUB_DIR)

from libraries.messengers.BaseZeroMqSocketContextManager import \
    BaseZeroMqSocketContextManager

MESSENGER_SERVER_NAME = 'messenger_server_REP'



def receive_messages():
    server = BaseZeroMqSocketContextManager(init_context=True)
    
    server.add_socket_to_context(socket_name=MESSENGER_SERVER_NAME)
    
    timeout = 0

    server.bind_socket_to_address(MESSENGER_SERVER_NAME, 
                                  address_port=MESSENGER_SERVER_PORT)

    while timeout <= 60:
        message = server.receive_message(MESSENGER_SERVER_NAME)

        print(MESSAGE_SENT_TEXT.format(cli=message[0].decode(), msg=message[1].decode()))
        
        server.send_message(MESSENGER_SERVER_NAME, message[1], 
                            received_from=message[0].decode())

        timeout += 1




if __name__ == '__main__':
    receive_messages()

