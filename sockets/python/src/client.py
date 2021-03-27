import socket
from socket import AF_INET, SOCK_STREAM


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
        
        print("Connected done")


def generate_matrix(m: int, n: int) -> list:
    matrix = []
    
    for line in range(0, m):
        matrix.append([])
        for column in range(0, n):
            matrix[line].append(randint(1, 11))
    
    return matrix


def send_matrix_lines(a_line: list, b_line: list):
    for client in CLIENTS:
        if not client.state:
            clien.state = True
            client.send()
            client.recv()
            client.state = False


if __name__ == '__main__':
    # matrix_lines = int(input("Type the matrixes' line quantity: "))
    # matrix_columns = int(input("Type the matrixes' column quantity: "))

    # matrix_a = generate_matrix(matrix_lines, matrix_columns)
    # matrix_b = generate_matrix(matrix_lines, matrix_columns)

    start_connections()
    
    # print(matrix_a)
        
    # print(matrix_b)

  
    