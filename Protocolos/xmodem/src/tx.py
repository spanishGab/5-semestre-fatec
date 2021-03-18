import os
import serial
import math
from Packet import Packet
from common_constants import *

def transfer_file(port_path: str, file_path: str):
    tx = serial.Serial(port=port_path)

    transference_begin = tx.readline().replace(END_OF_LINE, b'')
    
    if transference_begin != NAK:
        print("No NAK byte was received. Finishing transference process")
        return
    

    file_size = os.stat(file_path).st_size
    packet_quantity = math.ceil(file_size / 128)

    with open(file_path, mode='r', encoding='ASCII') as reader:
        for i, p in enumerate(range(1, packet_quantity+1)):
            data = reader.read(128)
            
            packet = Packet(bin(i)[2:].encode(), data)

            tx.write(packet.soh+END_OF_LINE)

            tx.write(packet.seq_number+END_OF_LINE)

            tx.write(packet.compliment_seq_number+END_OF_LINE)

            tx.write(packet.data+END_OF_LINE)

            tx.write(str(packet.checksum).encode())

            sequence_out_of_order = tx.readline().replace(END_OF_LINE, b'')
            if sequence_out_of_order == CAN:
                print("The packet sequence number sent was incorrect. "+
                    " Finishing transference process")
                return
            
            checksum_result = tx.readline().replace(END_OF_LINE, b'')
            if checksum_result == NAK:
                print("The packet bytes sent was incomplete. "+
                    " Finishing transference process")
                return
    
    transaction_complete = tx.readline().replace(END_OF_LINE, b'')

    if transaction_complete == NAK:
        tx.write(EOT+END_OF_LINE)
    
    if tx.readline().replace(END_OF_LINE, b'') == ACK:
        print("File transference succeded!")

                





