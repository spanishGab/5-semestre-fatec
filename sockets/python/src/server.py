import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR

from constants import *

from concurrent.futures import ThreadPoolExecutor


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
    for server in SERVERS.keys():
        # binding the server to its port and host
        SERVERS[server]['tcp'].bind((HOST, SERVERS[server]['port']))
        # listening to connection attempts
        SERVERS[server]['tcp'].listen(1)

    # starting the client - server connections
    for server in SERVERS.values():
        print(PORT_MESSAGE.format(port=server['port'], msg="trying to connect"))

        server['conn'], _ = server['tcp'].accept()
        
        print(PORT_MESSAGE.format(port=server['port'], msg="connection done"))


def shutdown_connections():
    # shutting down the client - server connections
    for server in SERVERS.values():
        print(PORT_MESSAGE.format(port=server['port'], msg="shutting down"))
        server['conn'].shutdown(SHUT_RDWR)


def receive_matrices_lines(server: dict) -> tuple:
    print(PORT_MESSAGE.format(port=server['port'], msg="reading matrices lines"))
    
    lines = server['conn'].recv(MAX_BUFFER_SIZE).decode()
    
    print(PORT_MESSAGE.format(port=server['port'], msg="lines read"))

    # preparing lines to be added
    lines = lines.split(LINE_SEP)

    a_line = eval(lines[0])

    b_line = eval(lines[1])

    return (a_line, b_line)


def calculate_lines_sum(a_line: list, b_line: list) -> list:
    result_line = []
    
    for i in range(0, len(a_line)):
        result_line.append(a_line[i] + b_line[i])
    
    return result_line


def make_lines_transference(server: dict) -> object:
    # awaits for lines until client doesn't send any more
    while True:
        # waiting for a STX byte to start the transference
        print(PORT_MESSAGE.format(port=server['port'], msg="waiting for a STX byte"))
        transference_start = server['conn'].recv(1)

        # checking whether the STX byte was received
        if transference_start == STX:
            print(PORT_MESSAGE.format(port=server['port'], msg="STX rceived"))
            
            # sending the ACK byte to confirm transference begin
            print(PORT_MESSAGE.format(port=server['port'], msg="sending ACK byte"))
            server['conn'].send(ACK)
        else:
            print(PORT_MESSAGE.format(port=server['port'], 
                msg="could not start transference, aborting!"))
            return None

        # receiving matrices lines
        a_line, b_line = receive_matrices_lines(server)

        # calculating lines sum
        print(PORT_MESSAGE.format(port=server['port'], msg="calculating lines sum"))
        result_line = calculate_lines_sum(a_line, b_line)

        # preparing to send the result to the client
        result_line = str(result_line)

        print(PORT_MESSAGE.format(port=server['port'], msg="sending results"))
        server['conn'].send(result_line.encode())

        print(PORT_MESSAGE.format(port=server['port'], 
            msg="waiting for an ACK byte"))
        receivement_confirmation = server['conn'].recv(1)
        
        if receivement_confirmation == ACK:
            print(PORT_MESSAGE.format(port=server['port'], msg="ACK received"))

            print(PORT_MESSAGE.format(port=server['port'], 
                msg="results sent successfully"))

            # sending an EOT byte to confirm transference end
            server['conn'].send(EOT)
        else:
            print(PORT_MESSAGE.format(port=server['port'], 
                msg="an error occoured while sendind results, aborting!"))
            return None


if __name__ == '__main__':
    start_connections()

    try:
        # starting the transferences
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(make_lines_transference, SERVERS['server_1'])
            executor.submit(make_lines_transference, SERVERS['server_2'])
            executor.submit(make_lines_transference, SERVERS['server_3'])
    except Exception as e:
        shutdown_connections()
        raise e
    finally:
        shutdown_connections()


    