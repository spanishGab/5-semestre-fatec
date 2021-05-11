from zmq import REQ
import zmq
from constants import (MESSENGER_SERVER_PORT, EMPTY_STRING,
                       RECEPTION_CONFIRMATION_MESSAGE)

from utils import print_message

from libraries.messengers.BaseZeroMqSocketContextManager import \
    BaseZeroMqSocketContextManager

MESSENGER_SERVER_NAME = 'messenger_server'


def start_communication():
    server = BaseZeroMqSocketContextManager(init_context=True)

    server.add_socket_to_context(socket_name=MESSENGER_SERVER_NAME)

    server.bind_socket_to_address(MESSENGER_SERVER_NAME,
                                  address_port=MESSENGER_SERVER_PORT)

    actual_message = EMPTY_STRING.encode()

    while actual_message.decode().capitalize() != 'Beye':
        message = server.receive_message(MESSENGER_SERVER_NAME)

        message_sender = message[0].decode()
        actual_message = message[1]
        message_recipient = message[2].decode()

        server.send_message(MESSENGER_SERVER_NAME,
                            RECEPTION_CONFIRMATION_MESSAGE)

        print_message(actual_message.decode(), message_sender)

        server.add_socket_to_context(message_recipient, socket_type=REQ)

        server.connect_socket_to_address(message_recipient,
                                         address_port=message_recipient)

        server.send_message(message_recipient, actual_message,
                            message_sender=message_sender)

        server.disconnect_socket_from_address(message_recipient)

        server.remove_socket_from_context(message_recipient)

    server.unbind_socket_from_address(MESSENGER_SERVER_NAME)


if __name__ == '__main__':
    start_communication()
