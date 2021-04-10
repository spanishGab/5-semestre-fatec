import os
import serial
import math
from Packet import Packet
from common_constants import *

def transfer_file(port_path: str, file_path: str):
    tx = serial.Serial(port=port_path)

    # waiting ffor a NAK char to begin the file transference
    transference_begin = tx.read(1)

    # checking whether the reciver char is not a NAK
    if transference_begin != NAK:
        print(transference_begin.decode())
        print("No NAK byte was received. Finishing transference process")
        return
    
    # getting the file size in bytes and calculating the packet
    # quantity based on it
    file_size = os.stat(file_path).st_size
    packet_quantity = math.ceil(file_size / 128)
    
    print("Packet quantity: "+str(packet_quantity))

    # instantiating an empty Packet class
    packet = Packet()
    
    # starting the file transference
    with open(file_path, mode='r', encoding='ASCII') as reader:
        for pq in range(1, packet_quantity+1):
            # reading 128 bytes from the file
            data = reader.read(128)

            # instantiating a new packet
            packet.packet_number = pq
            packet.data = data
            packet.set_packet_number_compliment()
            packet.set_checksum()

            # sending a SOH char to RX
            tx.write(packet.soh)

            # sending the packet number to RX
            tx.write(packet.packet_number)

            # sending the packet number compliment to RX
            tx.write(packet.packet_number_compliment)

            # sending the packet data to RX
            tx.write(packet.data)

            # sending the packet checksum to RX
            tx.write(packet.checksum)

            # witing for a ACK char to validade the transference
            transference_response = tx.read(1)
            
            # checking whether the received char is a CAN, indicating
            # the transference end
            if transference_response == CAN:
                print("The packet sequence number sent was incorrect. "+
                    " Finishing transference process")
                return
            
            # checking whether the received char is a NAK, indicating
            # the transference end
            if transference_response == NAK:
                print("The packet bytes sent was incomplete. "+
                    " Finishing transference process")
                return
            
            print(f"Packet {pq} sent, {packet_quantity-pq} left")
            
        # sending an EOT char to indicate the end of the transmission
        tx.write(EOT)

    # checking for thr end off transmition
    if tx.read(1) == ACK:
        print("File transference succeded!")


if __name__ == '__main__':
    port_number = input("Type the port number: ")
    port = DEFAULT_PORT_PATH+port_number

    file_path = input("Type the file path you want to transfer "+
        "based on your home directory: ")
    
    file_path = os.path.join(USER_HOME, file_path)
    transfer_file(port, file_path)
