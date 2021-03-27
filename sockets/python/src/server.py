import socket
from socket import AF_INET, SOCK_STREAM


HOST = '127.0.0.1'

SERVERS = {
    'server_1': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5000, 
        'conn': None
    },

    'server_2': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5001, 
        'conn': None
    },

    'server_3': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5002, 
        'conn': None
    },
}

def start_connections():
    for server in SERVERS.values():
        print("Trying to connect")
        
        server['tcp'].bind((HOST, server['port']))
        server['tcp'].listen(1)
        server['conn'], _ = server['tcp'].accept()
        
        print("Connected done")

if __name__ == '__main__':
    start_connections()