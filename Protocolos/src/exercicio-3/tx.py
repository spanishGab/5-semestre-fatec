import serial
import os
from pathlib import Path
from common_constants import *

HOME_DIR = os.environ['HOME'] if os.environ['HOME'] is not None else '~'
SOURCE_DIR_NAME = 'Source'
SOURCE_FILES_DIR = os.path.join(HOME_DIR, SOURCE_DIR_NAME)
BASE_PORT_PATH = "/dev/pts/"
TRANSFERENCES_SUCCEDED = "transferencia de arquivos realizada com sucesso"
FILE_NAME_NOT_SENT = "falha ao enviar nome de arquivo"
FILE_LINE_NOT_SENT = "falha ao enviar linha de arquivo"

def transfer_files(serial_port_number: str):
    tx = serial.Serial(BASE_PORT_PATH+serial_port_number)

    tx.write(STARTING_TRANSFERENCE)

    # checking whether the RX is not able to begin the file transfernce
    if tx.readline() != ABLE_TO_RECEIVE:
        print(UNABLE_TO_TRANSFER)
    
    # getting the quantity of files to send
    file_quantity = len(os.listdir(SOURCE_FILES_DIR))

    # sending the file quantity to RX
    tx.write((str(file_quantity)+'\n').encode())

    # checking if the files quantity was received from RX
    file_quantity_response = tx.readline()
    if file_quantity_response != FILE_QUANTITY_RECEIVED:
        print(file_quantity_response.decode())
        return
    
    for file_details in Path(SOURCE_FILES_DIR).glob('*'):
        # sending the file name to RX
        tx.write((file_details.name+'\n').encode())
        
        if tx.readline() != FILE_NAME_RECEIVED:
            print(FILE_NAME_NOT_SENT)
            return
        
        with open(file_details.absolute(),
            mode='r',
            encoding='ASCII'
        ) as file_transfer:
            for line in file_transfer:
                if '\n' not in line:
                    line += '\n'
                tx.write(line.encode())
            
                if tx.readline() != FILE_LINE_RECEIVED:
                    print(FILE_LINE_NOT_SENT)
                    return
            
            tx.write(END_OF_FILE)


    print(tx.readline().decode())

    tx.write(RESULTS_RECEIVED)

    print(TRANSFERENCES_SUCCEDED)


if __name__ == '__main__':
    print("""Welcome to the SFTP (Simple File Transfer Protocol).
    Put the files you want to transfer into the ~/Source directory""")

    if not os.path.isdir(SOURCE_FILES_DIR):
        os.mkdir(SOURCE_FILES_DIR)

    tx_port = input("Type the TX port number: ")
    transfer_files(tx_port)

