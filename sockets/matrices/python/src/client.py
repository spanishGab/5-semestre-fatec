import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR

from random import randint

from threading import Semaphore, Thread
from concurrent.futures import ThreadPoolExecutor

from constants import *

result_matrix = []
SEMAPHORE = Semaphore(1)

CLIENTS = {
    'client_1': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5000
    },

    'client_2': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5001
    },

    'client_3': {
        'tcp': socket.socket(family=AF_INET, type=SOCK_STREAM), 
        'port': 5002
    },
}


def start_connections():
    # starting the client - server connections
    for client in CLIENTS.values():
        print(PORT_MESSAGE.format(port=client['port'], msg="trying to connect"))
                
        client['tcp'].connect((HOST, client['port']))
        
        print(PORT_MESSAGE.format(port=client['port'], msg="connection done"))


def shutdown_connections():
    # shutting down the client - server connections
    for client in CLIENTS.values():
        print(PORT_MESSAGE.format(port=client['port'], msg="shutting down"))
        client['tcp'].shutdown(SHUT_RDWR)


def generate_matrix(m: int, n: int) -> list:
    matrix = []
    
    for line in range(0, m):
        matrix.append([])
        for column in range(0, n):
            matrix[line].append(randint(1, 9))
    
    return matrix


def make_lines_transferecne(client: dict, lines: bytes) -> object:
    # sending a STX byte to indicate the transference begin
    print(PORT_MESSAGE.format(port=client['port'], msg="sending STX byte"))
    client['tcp'].send(STX)

    # receiving the ACK byte from the server
    print(PORT_MESSAGE.format(port=client['port'], msg="waiting for an ACK byte"))
    transference_start = client['tcp'].recv(1)

    # checking whether the ACK byte was received
    if transference_start == ACK:
        print(PORT_MESSAGE.format(port=client['port'], msg="ACK received"))
        print(PORT_MESSAGE.format(port=client['port'], msg="starting transference"))

        # sending the matrices lines to the server
        print(PORT_MESSAGE.format(port=client['port'], msg="sending matrices lines"))
        client['tcp'].send(lines)
        
        # receiving the sum result linef from the server
        print(PORT_MESSAGE.format(port=client['port'], msg="reeceiving result line"))
        
        sum_results = client['tcp'].recv(MAX_BUFFER_SIZE)
        
        print(PORT_MESSAGE.format(port=client['port'], msg="result line received"))

        # checking whether the sum results were received
        if sum_results:
            client['tcp'].send(ACK)
        else:
            print(PORT_MESSAGE.format(port=client['port'], 
                msg="failed to receive the sum results, aborting!"))
            return None

        # receiving the transference confirmation from the server
        print(PORT_MESSAGE.format(port=client['port'], 
                msg="waiting for an EOT byte"))
        transference_confirmation = client['tcp'].recv(1)
        
        if transference_confirmation == EOT:
            print(PORT_MESSAGE.format(port=client['port'], msg="EOT received"))
            
            print(PORT_MESSAGE.format(port=client['port'], 
                msg="transference succeded"))
            
            return sum_results
        
        else:
            print(PORT_MESSAGE.format(port=client['port'], 
                msg="An error occoured while receiving the transference "+
                    "confirmation, aborting!"))
            return None
    else:
        print(PORT_MESSAGE.format(port=client['port'], 
            msg="could not start transference"))
        return None


def sum_matrices_lines(line_index: int, 
                       client: dict, 
                       a_line: list, 
                       b_line: list) -> list:
    global result_matrix

    # preparing the matrices lines to be transfered
    a_line = str(a_line)

    b_line = str(b_line)

    lines_to_sum = (a_line+LINE_SEP+b_line).encode()
    
    # obtaining the sum results
    sum_results = make_lines_transferecne(client, lines_to_sum)

    sum_results = eval(sum_results.decode())
    
    SEMAPHORE.acquire()
    print(PORT_MESSAGE.format(port=client['port'], msg="storing results"))
    result_matrix.append((line_index, sum_results))
    SEMAPHORE.release()


if __name__ == '__main__':
    matrix_lines = int(input("Type the matrices' line quantity: "))
    matrix_columns = int(input("Type the matrices' column quantity: "))

    matrix_a = generate_matrix(matrix_lines, matrix_columns)
    
    # print(matrix_a[0][0:5]) #! uncomment to get the first 5 elements (for big  matrices)
    # print(matrix_a[-1][-5:]) #! uncomment to get the last 5 elements (for big  matrices)
    print('\n')
    print("Matrix A")
    for line in matrix_a:
        print(line)
    print('\n')
    
    matrix_b = generate_matrix(matrix_lines, matrix_columns)
    
    # print(matrix_b[0][0:5]) #! uncomment to get the first 5 elements (for big  matrices)
    # print(matrix_b[-1][-5:]) #! uncomment to get the last 5 elements (for big  matrices) 
    print("Matrix B")
    for line in matrix_b:
        print(line)
    print('\n')
    
    start_connections()

    try:
        for i in range(0, matrix_lines, 3):
            t1 = Thread(target=sum_matrices_lines, args=(i, CLIENTS['client_1'],
                matrix_a[i], matrix_b[i]))
            t1.start()
            t1.join()
            
            try:
                t2 = Thread(target=sum_matrices_lines, args=(i+1, 
                    CLIENTS['client_2'], matrix_a[i+1], matrix_b[i+1]))
                t2.start()
                t2.join()
            except IndexError:
                break
            
            try:
                t3 = Thread(target=sum_matrices_lines, args=(i+2, 
                    CLIENTS['client_3'], matrix_a[i+2], matrix_b[i+2]))
                t3.start()
                t3.join()
            except IndexError:
                break
            
        result_matrix.sort(key=lambda matrix: matrix[0])
        print('\n')
        for _, line in result_matrix:
            print(line)
        print('\n')

        # print(result_matrix[0][1][0:5]) #! uncomment to get the first 5 elements (for big  matrices)
        # print(result_matrix[-1][1][-5:]) #! uncomment to get the last 5 elements (for big  matrices)
    except Exception as e:
        shutdown_connections()
        raise e
    finally:
        shutdown_connections()

    
        

  
    