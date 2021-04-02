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
    # print("Reading matrices lines")
    lines = conn.recv(MAX_BUFFER_SIZE).decode()
    # print("Lines reead")

    lines = lines.split(LINE_SEP)

    # print("Eval a_line")
    a_line = eval(lines[0])
    
    # print("Eval b_line")
    b_line = eval(lines[1])

    # print("Returning a_line, b_line")
    return (a_line, b_line)


def calculate_lines_sum(a_line: list, b_line: list) -> list:
    result_line = []
    
    for i in range(0, len(a_line)):
        result_line.append(a_line[i] + b_line[i])
    
    return result_line


def make_lines_transference(server: dict):
    while True:
        print("Waiting for a STX, port: ", server['port'])
        transference_start = server['conn'].recv(1)
        # print("Got: ", str(transference_start))

        if transference_start == STX:
            print("Sending ACK to the client")
            server['conn'].send(ACK)
        else:
            print("Could not start transference")
            return

        # print("Receiving matrices lines")
        a_line, b_line = receive_matrices_lines(server['conn'])
        # print("Lines rceived")

        # print("Calculating sum")
        result_line = calculate_lines_sum(a_line, b_line)
        # print("Sum calculated")

        result_line = str(result_line)

        server['conn'].send(result_line.encode())

        receivement_confirmation = server['conn'].recv(1)
        
        if receivement_confirmation == ACK:
            print("Results sent successfully")
            server['conn'].send(EOT)
        else:
            print("An error occoured while sendind results")
            return



if __name__ == '__main__':
    start_connections()

    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(make_lines_transference, SERVERS['server_1'])
            executor.submit(make_lines_transference, SERVERS['server_2'])
            executor.submit(make_lines_transference, SERVERS['server_3'])
    except Exception as e:
        print(str(e))
        shutdown_connections()
    finally:
        shutdown_connections()


    