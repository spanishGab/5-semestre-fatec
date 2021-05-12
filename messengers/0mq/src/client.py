from zmq import REQ
from constants import (MESSENGER_SERVER_INTERFACE, MESSENGER_SERVER_PROTOCOL,
                       MESSENGER_SERVER_PORT, EMPTY_STRING, BEYE_MESSAGE,
                       CONTACTS, RECEPTION_CONFIRMATION_MESSAGE, MESSAGE_SPACE)

from utils import print_message

from libraries.messengers.BaseZeroMqSocketContextManager import \
    BaseZeroMqSocketContextManager

client_a = BaseZeroMqSocketContextManager(init_context=True)

SERVER_ALIAS = 'srv'


def start_communication(sender_name: str,
                        sender_protocol: str,
                        sender_interface: str,
                        sender_port: int,
                        recipient_name: str,
                        recipient_protocol: str,
                        recipient_interface: str,
                        recipient_port: int):

    cient_server_socket_name = sender_name+SERVER_ALIAS

    client_a.add_socket_to_context(socket_name=sender_name, socket_type=REQ)
    client_a.add_socket_to_context(socket_name=cient_server_socket_name)

    client_a.connect_socket_to_address(
        socket_name=sender_name,
        address_protocol=MESSENGER_SERVER_PROTOCOL,
        address_interface=MESSENGER_SERVER_INTERFACE,
        address_port=MESSENGER_SERVER_PORT
    )

    client_a.bind_socket_to_address(socket_name=cient_server_socket_name,
                                    address_protocol=sender_protocol,
                                    address_interface=sender_interface,
                                    address_port=sender_port)

    actual_message = EMPTY_STRING

    while actual_message.capitalize() != BEYE_MESSAGE:
        message = input(MESSAGE_SPACE + "You: ")

        if message == EMPTY_STRING:
            message = client_a.receive_message(cient_server_socket_name)

            message_sender = message[0]
            actual_message = message[1]

            print_message(actual_message, message_sender)

            client_a.send_message(cient_server_socket_name,
                                  RECEPTION_CONFIRMATION_MESSAGE)
        else:
            client_a.send_message(
                sender_name,
                message,
                message_sender=sender_name,
                message_recipient_name=recipient_name,
                message_recipient_protocol=recipient_protocol,
                message_recipient_interface=recipient_interface,
                message_recipient_port=recipient_port
            )

            client_a.receive_message(sender_name)

            actual_message = message

    client_a.disconnect_socket_from_address(sender_name)


if __name__ == '__main__':
    sender_name = input("Type your name: ")

    recipient_name = input(
        "Enter the contact with whom you want to communicate: ")

    try:
        sender_protocol = CONTACTS[sender_name]['protocol']
        sender_interface = CONTACTS[sender_name]['interface']
        sender_port = CONTACTS[sender_name]['port']
    except KeyError:
        print("You are not registered on the RawtsApp yet, aborting")
        quit()

    try:
        recipient_protocol = CONTACTS[recipient_name]['protocol']
        recipient_interface = CONTACTS[recipient_name]['interface']
        recipient_port = CONTACTS[recipient_name]['port']
    except KeyError:
        print("{recipient_name} doesn't exist on your contacts list, aborting")
        quit()

    start_communication(sender_name, sender_protocol, sender_interface,
                        sender_port, recipient_name, recipient_protocol,
                        recipient_interface, recipient_port)
