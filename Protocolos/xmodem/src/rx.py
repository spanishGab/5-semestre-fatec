import os
import serial
from common_constants import *
from Packet import Packet

TRANSFER_DIRECTORY = os.path.join(USER_HOME, 'Documentos')

def receive_file(port: str, file_name: str):
    rx = serial.Serial(port)

    # starting the transference by seending a NAK byte
    rx.write(NAK+END_OF_LINE)
    print("Sending NAK to TX\n")

    packet = Packet()

    received_line = rx.readline().replace(END_OF_LINE, b'')
    print("Receiving line from TX\n")
    
    while received_line != EOT:
        print("="*55)
        print("Starting to receive a packet\n")
        if received_line == SOH:
            try:
                print("\tGot a SOH char")

                pack_number = rx.readline().replace(END_OF_LINE, b'')
                print(f"\tPacket sequece_number: {pack_number}")

                pack_number_compliment = rx.readline().replace(END_OF_LINE, b'')
                print("\tPacket pack_number_compliment: "+
                    f"{pack_number_compliment}")

                data = rx.read(128)

                checksum = int(rx.readline().replace(END_OF_LINE, b'').decode())
                print(f"\tPacket checksum: {checksum}")
            except UnicodeDecodeError as ue:
                print(ue)
                rx.write(CAN+END_OF_LINE)

            packet.pack_number = int.from_bytes(pack_number, 'big')
            packet.data = data.decode()
            packet.set_pack_number_compliment()
            packet.set_checksum()

            if pack_number_compliment != packet.pack_number_compliment:
                print("\tThe packet compliment number received "+
                    f"({pack_number_compliment}) doesn't match the "+
                    f" calculated one ({packet.pack_number_compliment})")
                
                rx.write(CAN+END_OF_LINE)
            
            if checksum == packet.checksum:
                print("\tChecksum validated!")
                rx.write(ACK+END_OF_LINE)
                
                with open(os.path.join(TRANSFER_DIRECTORY, file_name),
                    mode='a+',
                    encoding='ASCII'
                ) as writer:
                    print("\tWriting the packet to the file")
                    writer.write(packet.data.decode())

            else:
                print(f"\tInvalid Checksum! {checksum} != {packet.checksum}")
                rx.write(NAK+END_OF_LINE)

        print("\nPacket successfully received\n")
        print("="*55)
        received_line = rx.readline().replace(END_OF_LINE, b'')
    
    rx.write(NAK+END_OF_LINE)
    
    transaction_complete = rx.readline().replace(END_OF_LINE, b'')
    
    if transaction_complete == EOT:
        rx.write(ACK+END_OF_LINE)


if __name__ == '__main__':
    port_number = input("Type the port number: ")
    port = DEFAULT_PORT_PATH+port_number

    file_name = input("Type the file name: ")
    receive_file(port, file_name)


