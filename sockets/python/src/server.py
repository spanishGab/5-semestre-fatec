import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR

from constants import *

from concurrent.futures import ThreadPoolExecutor

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
    SERVERS['server_1']['tcp'].bind((HOST, SERVERS['server_1']['port']))
    SERVERS['server_2']['tcp'].bind((HOST, SERVERS['server_2']['port']))
    SERVERS['server_3']['tcp'].bind((HOST, SERVERS['server_3']['port']))

    SERVERS['server_1']['tcp'].listen(1)
    SERVERS['server_2']['tcp'].listen(1)
    SERVERS['server_3']['tcp'].listen(1)

    for server in SERVERS.values():
        print("Trying to connect")

        server['conn'], _ = server['tcp'].accept()
        
        print("Connection done")


def shutdown_connections():
    for server in SERVERS.values():
        server['conn'].shutdown(SHUT_RDWR)


def receive_matrices_lines(conn: socket.socket) -> tuple:
    lines = conn.recv(1024).decode()

    lines = lines.split(LINE_SEP)

    a_line = eval(lines[0])
    
    b_line = eval(lines[1])

    return (a_line, b_line)


def calculate_lines_sum(conn: socket.socket) -> list:
    a_line, b_line = receive_matrices_lines(conn)

    result_line = []
    
    for i in range(0, len(a_line)):
        result_line.append(a_line[i] + b_line[i])
    
    return result_line


def make_lines_transference(conn: socket.socket):
    while True:
        print("Waiting for a STX")
        transference_start = conn.recv(1)

        if transference_start == STX:
            print("Sending ACK to the client")
            conn.send(ACK)
        else:
            print("Could not start transference")
            return

        result_line = calculate_lines_sum(conn)

        result_line = str(result_line)

        conn.send(result_line.encode())

        receivement_confirmation = conn.recv(1)
        
        if receivement_confirmation == ACK:
            print("Results sent successfully")
            conn.send(EOT)
        else:
            print("An error occoured while sendind results")
            return



if __name__ == '__main__':
    start_connections()

    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            for _ in range(0, 3):
                executor.submit(make_lines_transference, SERVERS['server_1']['conn'])
                executor.submit(make_lines_transference, SERVERS['server_2']['conn'])
                executor.submit(make_lines_transference, SERVERS['server_3']['conn'])
    except Exception as e:
        print(str(e))
        shutdown_connections()
    finally:
        shutdown_connections()


    