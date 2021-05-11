from zmq import REQ
from constants import (MESSENGER_SERVER_PORT, EMPTY_STRING,
                       CONTACTS_PORTS, RECEPTION_CONFIRMATION_MESSAGE)

from utils import print_message

from libraries.messengers.BaseZeroMqSocketContextManager import \
    BaseZeroMqSocketContextManager

client_a = BaseZeroMqSocketContextManager(init_context=True)

SERVER_ALIAS = 'srv'


def start_communication(client_name: str,
                        client_port: int,
                        recipient_port: int):
    client_a.add_socket_to_context(socket_name=client_name, socket_type=REQ)
    client_a.add_socket_to_context(socket_name=(client_name+SERVER_ALIAS))

    client_a.connect_socket_to_address(client_name,
                                       address_port=MESSENGER_SERVER_PORT)

    client_a.bind_socket_to_address(client_name+SERVER_ALIAS,
                                    address_port=client_port)

    actual_message = EMPTY_STRING.encode()

    while actual_message.decode().capitalize() != 'Beye':
        message = input(
            f"{client_name}, Type your message or hit ENTER to " +
            "wait for a mesage to arive: "
        ).encode()

        if message.decode() == EMPTY_STRING:
            message = client_a.receive_message(client_name+SERVER_ALIAS)

            message_sender = message[0].decode()
            actual_message = message[1]

            print_message(actual_message.decode(), message_sender)

            client_a.send_message(client_name+SERVER_ALIAS,
                                  RECEPTION_CONFIRMATION_MESSAGE)
        else:
            client_a.send_message(client_name, message,
                                  message_sender=client_name,
                                  message_recipient=recipient_port)

            client_a.receive_message(client_name)

            actual_message = message

    client_a.disconnect_socket_from_address(client_name)


if __name__ == '__main__':
    sender_name = input("Type your name: ")

    contact_name = input(
        "Enter the contact with whom you want to communicate: ")

    try:
        sender_port = CONTACTS_PORTS[sender_name]
    except KeyError:
        print("You are not registered on the RawtsApp yet, aborting")
        quit()

    try:
        contact_port = CONTACTS_PORTS[contact_name]
    except KeyError:
        print("{contact_name} doesn't exist on your contacts list, aborting")
        quit()

    start_communication(sender_name, sender_port, contact_port)
