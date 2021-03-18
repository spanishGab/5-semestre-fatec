import serial
from common_constants import *
from Packet import Packet

def receive_file(port: str):
    rx = serial.Serial(port)

    # starting the transference by seending a NAK byte
    rx.write(NAK+END_OF_LINE)

    received_line = rx.readline().replace(END_OF_LINE, b'')
    while receive_file != EOT:
        if received_line == SOH:
            sequence_number = rx.readline().replace(END_OF_LINE, b'')

            compliment_sequence_number = rx.readline().replace(END_OF_LINE, b'')

            data = rx.readline().decode()

            checksum = int(rx.readline().replace(END_OF_LINE, b'').decode())

            packet = Packet(sequence_number, data)

            if compliment_sequence_number != packet.compliment_seq_number:
                rx.write(CAN+END_OF_LINE)
            
            if checksum == packet.checksum:
                rx.write(ACK+END_OF_LINE)
            else:
                rx.write(NAK+END_OF_LINE)

        received_line = rx.readline().replace(END_OF_LINE, b'')
    
    rx.write(NAK+END_OF_LINE)
    
    transaction_complete = rx.readline().replace(END_OF_LINE, b'')
    
    if transaction_complete == EOT:
        rx.write(ACK+END_OF_LINE)






