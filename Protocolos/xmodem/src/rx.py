import os
import serial
from common_constants import *
from Packet import Packet

TRANSFER_DIRECTORY = os.path.join(USER_HOME, 'Documentos')

def receive_file(port: str):
    rx = serial.Serial(port)

    # starting the transference by seending a NAK byte
    rx.write(NAK+END_OF_LINE)
    print("Sending NAK to TX\n")

    packet = Packet()

    received_line = rx.readline().replace(END_OF_LINE, b'')
    print("Receiving line from TX\n")
    
    while received_line != EOT:
        print("Starting to receive a packet\n")
        if received_line == SOH:
            try:
                print("Got a SOH char\n")

                pack_number = rx.readline().replace(END_OF_LINE, b'')
                print(f"Packet sequece_number: {pack_number}\n")

                pack_number_compliment = rx.readline().replace(END_OF_LINE, b'')
                print("Packet pack_number_compliment: "+
                    f"{pack_number_compliment}\n")

                data = rx.read(128)
                print(f"Packet data: {data}\n")

                checksum = int(rx.readline().replace(END_OF_LINE, b'').decode())
                print(f"Packet checksum: {checksum}")
            except UnicodeDecodeError:
                print("UnicodeError")

            packet.pack_number = int.from_bytes(pack_number, 'big')
            packet.data = data.decode()
            packet.set_pack_number_compliment()
            packet.set_checksum()

            if pack_number_compliment != packet.pack_number_compliment:
                print("The packet compliment number received "+
                    f"({pack_number_compliment}) doesn't match the "+
                    f" calculated one ({packet.pack_number_compliment})")
                
                rx.write(CAN+END_OF_LINE)
            
            if checksum == packet.checksum:
                print("Checksum validated!")
                rx.write(ACK+END_OF_LINE)
                
                with open(os.path.join(TRANSFER_DIRECTORY, 'transfr.txt'),
                    mode='a+',
                    encoding='ASCII'
                ) as writer:
                    print("Writing the packet to a file")
                    writer.write(packet.data.decode())

            else:
                print(f"Checksum invalid! {checksum} != {packet.checksum}")
                rx.write(NAK+END_OF_LINE)

        received_line = rx.readline().replace(END_OF_LINE, b'')
    
    rx.write(NAK+END_OF_LINE)
    
    transaction_complete = rx.readline().replace(END_OF_LINE, b'')
    
    if transaction_complete == EOT:
        rx.write(ACK+END_OF_LINE)


if __name__ == '__main__':
    port_number = input("Type the port number: ")
    port = DEFAULT_PORT_PATH+port_number
    receive_file(port)


