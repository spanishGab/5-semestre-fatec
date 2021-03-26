import os
import serial
import math
from Packet import Packet
from common_constants import *

def transfer_file(port_path: str, file_path: str):
    tx = serial.Serial(port=port_path)

    transference_begin = tx.readline().replace(END_OF_LINE, b'')

    if transference_begin != NAK:
        print(transference_begin.decode())
        print("No NAK byte was received. Finishing transference process")
        return
    

    file_size = os.stat(file_path).st_size
    packet_quantity = math.ceil(file_size / 128)
    print("Packet quantity: "+str(packet_quantity))

    packet = Packet()
    with open(file_path, mode='r', encoding='ASCII') as reader:
        for pq in range(1, packet_quantity+1):
            data = reader.read(128)

            packet.pack_number = pq
            packet.data = data
            packet.set_pack_number_compliment()
            packet.set_checksum()

            tx.write(packet.soh+END_OF_LINE)

            tx.write(packet.pack_number+END_OF_LINE)

            tx.write(packet.pack_number_compliment+END_OF_LINE)

            tx.write(packet.data)

            tx.write(str(packet.checksum).encode()+END_OF_LINE)

            transference_response = tx.readline().replace(END_OF_LINE, b'')
            if transference_response == CAN:
                print("The packet sequence number sent was incorrect. "+
                    " Finishing transference process")
                return
            
            if transference_response == NAK:
                print("The packet bytes sent was incomplete. "+
                    " Finishing transference process")
                return
            
            print(f"Packet {pq} sent, {packet_quantity-pq} left")
            
        tx.write(EOT+END_OF_LINE)
    
    transaction_complete = tx.readline().replace(END_OF_LINE, b'')

    if transaction_complete == NAK:
        tx.write(EOT+END_OF_LINE)
    
    if tx.readline().replace(END_OF_LINE, b'') == ACK:
        print("File transference succeded!")

if __name__ == '__main__':
    port_number = input("Type the port number: ")
    port = DEFAULT_PORT_PATH+port_number

    file_path = input("Type the file path you want to transfer "+
        "based on your home directory: ")
    
    file_path = os.path.join(USER_HOME, file_path)
    transfer_file(port, file_path)
