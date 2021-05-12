from zmq import REQ
from constants import (MESSENGER_SERVER_PROTOCOL, MESSENGER_SERVER_INTERFACE,
                       MESSENGER_SERVER_PORT, EMPTY_STRING, BEYE_MESSAGE,
                       RECEPTION_CONFIRMATION_MESSAGE)

from utils import print_message

from libraries.messengers.BaseZeroMqSocketContextManager import \
    BaseZeroMqSocketContextManager

MESSENGER_SERVER_NAME = 'messenger_server'


def start_communication():
    server = BaseZeroMqSocketContextManager(init_context=True)

    server.add_socket_to_context(socket_name=MESSENGER_SERVER_NAME)

    server.bind_socket_to_address(
        socket_name=MESSENGER_SERVER_NAME,
        address_protocol=MESSENGER_SERVER_PROTOCOL,
        address_interface=MESSENGER_SERVER_INTERFACE,
        address_port=MESSENGER_SERVER_PORT
    )

    actual_message = EMPTY_STRING

    while actual_message.capitalize() != BEYE_MESSAGE:
        message = server.receive_message(MESSENGER_SERVER_NAME)

        message_sender = message[0]
        actual_message = message[1]
        message_recipient_name = message[2]
        message_recipient_protocol = message[3]
        message_recipient_interface = message[4]
        message_recipient_port = int(message[5])

        server.send_message(MESSENGER_SERVER_NAME,
                            RECEPTION_CONFIRMATION_MESSAGE)

        print_message(actual_message, message_sender)

        server.add_socket_to_context(socket_name=message_recipient_name,
                                     socket_type=REQ)

        server.connect_socket_to_address(
            socket_name=message_recipient_name,
            address_protocol=message_recipient_protocol,
            address_interface=message_recipient_interface,
            address_port=message_recipient_port)

        server.send_message(
                message_recipient_name,
                actual_message,
                message_sender=message_sender,
                message_recipient_protocol=message_recipient_protocol,
                message_recipient_interface=message_recipient_interface,
                message_recipient_port=message_recipient_port
            )

        server.disconnect_socket_from_address(message_recipient_name)

        server.remove_socket_from_context(message_recipient_name)

    server.unbind_socket_from_address(MESSENGER_SERVER_NAME)


if __name__ == '__main__':
    start_communication()
