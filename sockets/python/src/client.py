import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR

from random import randint

from threading import Semaphore
from concurrent.futures import ThreadPoolExecutor

from constants import *

SEMAPHORE = Semaphore(1)

HOST = '127.0.0.1'

CLIENTS = {
    'client_1': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5000, 
        'state': False
    },

    'client_2': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5001, 
        'state': False
    },

    'client_3': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5002, 
        'state': False
    },
}


def start_connections():
    for client in CLIENTS.values():
        print("Trying to connect")
        
        client['tcp'].connect((HOST, client['port']))
        
        print("Connection done")


def shutdown_connections():
    for client in CLIENTS.values():
        client['tcp'].shutdown(SHUT_RDWR)


def generate_matrix(m: int, n: int) -> list:
    matrix = []
    
    for line in range(0, m):
        matrix.append([])
        for column in range(0, n):
            matrix[line].append(randint(1, 11))
    
    return matrix


def make_lines_transferecne(lines: bytes) -> bytes:
    for client in CLIENTS.values():
        if not client['state']:

            client['tcp'].send(STX)

            print("Waiting for an ACK")
            transference_start = client['tcp'].recv(1)

            if transference_start == ACK:
                print("Starting to transfer, port", client['port'])
                client['state'] = True
                
                client['tcp'].send(lines)
                
                sum_results = client['tcp'].recv(1024)

                if sum_results:
                    client['tcp'].send(ACK)

                transference_confirmation = client['tcp'].recv(1)
                
                if transference_confirmation == EOT:
                    client['state'] = False
                    print("Received result: ", str(sum_results))
                    return sum_results
                
                else:
                    print("An error occoured while receiving the transference "+
                        "confirmation!")
                    return
            else:
                print("Could not start transference")
                return


def sum_matrices_lines(lines_index: int, a_line: list, b_line: list) -> list:
    a_line = str(a_line)

    b_line = str(b_line)

    lines_to_sum = (a_line+LINE_SEP+b_line).encode()
    
    sum_results = make_lines_transferecne(lines_to_sum)

    sum_results = eval(sum_results.decode())

    return (lines_index, sum_results)


if __name__ == '__main__':
    result_matrix = []

    matrix_lines = int(input("Type the matrices' line quantity: "))
    matrix_columns = int(input("Type the matrices' column quantity: "))

    matrix_a = generate_matrix(matrix_lines, matrix_columns)
    
    print('[')
    for line in matrix_a:
        print(line)
    print(']')
    
    matrix_b = generate_matrix(matrix_lines, matrix_columns)
    
    print('[')
    for line in matrix_b:
        print(line)
    print(']')
    
    start_connections()

    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(0, matrix_lines):
                res = executor.submit(sum_matrices_lines, i, matrix_a[i], matrix_b[i])
                
                result_matrix.append(res.result())
            
        result_matrix.sort(key=lambda matrix: matrix[0])
        for i, line in result_matrix:
            print(line)
    except Exception as e:
        print(str(e))
        shutdown_connections()
    finally:
        shutdown_connections()

    
        

  
    