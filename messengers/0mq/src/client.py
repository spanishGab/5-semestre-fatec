import sys
from constants import GITHUB_DIR, MESSENGER_SERVER_PORT

sys.path.insert(1, GITHUB_DIR)

from libraries.messengers.BaseZeroMqSocketContextManager import \
    BaseZeroMqSocketContextManager

from concurrent.futures import ThreadPoolExecutor

CLIENT_A_SERVER_NAME = "Gabriel"
CLIENT_A_PORT = 5001


def send_message(message: bytes):
    client_a = BaseZeroMqSocketContextManager(init_context=True)

    client_a.add_socket_to_context(socket_name=CLIENT_A_SERVER_NAME)
    
    print("Connecting to server")
    client_a.connect_socket_to_address(CLIENT_A_SERVER_NAME, 
                                       address_port=MESSENGER_SERVER_PORT)
    
    print("Sending message")
    client_a.send_message(CLIENT_A_SERVER_NAME, message)
    
    client_a.disconnect_socket_from_address(CLIENT_A_SERVER_NAME)


def receive_message():
    client_a = BaseZeroMqSocketContextManager(init_context=True)
    
    client_a.add_socket_to_context(socket_name=CLIENT_A_SERVER_NAME)
    
    client_a.connect_socket_to_address(CLIENT_A_SERVER_NAME, 
                                       address_port=MESSENGER_SERVER_PORT)

    while True:
        message = client_a.receive_message(CLIENT_A_SERVER_NAME)
        print(message.decode())
    
if __name__ == '__main__':
    #with ThreadPoolExecutor(max_workers=2) as executor:
    #    executor.submit(send_message, "HI".encode())
    #    executor.submit(receive_message)
    send_message("HI".encode())
    receive_message()