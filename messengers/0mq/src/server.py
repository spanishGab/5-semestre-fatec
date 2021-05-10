import sys
from constants import GITHUB_DIR, MESSENGER_SERVER_PORT

sys.path.insert(1, GITHUB_DIR)

from libraries.messengers.BaseZeroMqSocketContextManager import \
    BaseZeroMqSocketContextManager

MESSENGER_SERVER_NAME = 'messenger_server'
MESSAGE_SENT_TEXT = "{cli} Says: {msg}"


def receive_messages():
    server = BaseZeroMqSocketContextManager(init_context=True)
    
    server.add_socket_to_context(socket_name=MESSENGER_SERVER_NAME)
    
    server.bind_socket_to_address(MESSENGER_SERVER_NAME, 
                                  address_port=MESSENGER_SERVER_PORT)

    
    print("Waiting for message")
    message = server.receive_message(MESSENGER_SERVER_NAME)

    server.send_message(MESSENGER_SERVER_NAME, message[1], 
                        received_from=message[0])




if __name__ == '__main__':
    receive_messages()

