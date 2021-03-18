import serial
import os
from common_constants import *

HOME_DIR = os.environ['HOME'] if os.environ['HOME'] is not None else '~'
DESTINATION_DIR_NAME = 'Documentos'
DESTINATION_DIR = os.path.join(HOME_DIR, DESTINATION_DIR_NAME)
BASE_PORT_PATH = "/dev/pts/"
TRANSFERENCE_FAILED = "nao foi possivel receber confirmacao de transferencia\n".encode()
QUANTITY_ERROR = "falha no recebimento da quantidade de arquivos: "


def receive_files(serial_port_number: str):
    rx = serial.Serial(BASE_PORT_PATH+serial_port_number)

    # checking the starting transference message from TX
    if rx.readline() == STARTING_TRANSFERENCE:
        rx.write(ABLE_TO_RECEIVE)
    else:
        rx.write(UNABLE_TO_TRANSFER)
        print(UNABLE_TO_TRANSFER.decode())
        return
    
    try:
        # getting the quantity of files to transfer
        file_quantity = int(rx.readline().decode().replace('\n', ''))
        rx.write(FILE_QUANTITY_RECEIVED)
    except ValueError as ve:
        rx.write(QUANTITY_ERROR+ste(ve))
    

    transference_results = []
    try:
        while file_quantity > 0:
            # decoding the current file name
            file_name = rx.readline().decode().replace('\n', '')
            # sending a confirmation to TX
            rx.write(FILE_NAME_RECEIVED)

            open(os.path.join(DESTINATION_DIR, file_name),
                mode='w',
                encoding='ASCII').close()

            while True:
                with open(os.path.join(DESTINATION_DIR, file_name),
                    mode='a+',
                    encoding='ASCII'
                ) as transfer_file:
                    # decoding the file current line
                    file_line = rx.readline()

                    if file_line == END_OF_FILE: break

                    # writing the received line to the transfered file
                    transfer_file.write(file_line.decode())

                    # sending a confirmation to TX
                    rx.write(FILE_LINE_RECEIVED)
            
            transference_results.append(FILE_TRANSFERENCE_SUCCES.format(file_name))

            file_quantity -= 1
    except Exception as e:
        transference_results.append(FILE_TRANSFERENCE_ERROR.format(file_name, str(e)))
    
    
    rx.write((str(transference_results)+'\n').encode())
    
    if rx.readline() == RESULTS_RECEIVED:
        rx.write(TRANSFERENCES_END)
    else:
        rx.write(TRANSFERENCE_FAILED)


if __name__ == '__main__':
    rx_port = input("Type the TX port number: ")
    receive_files(rx_port)


