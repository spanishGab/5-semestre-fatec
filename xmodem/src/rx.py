import os
import serial
from common_constants import *
from Packet import Packet

DESTINATION_DIR = os.path.join(os.path.split(__file__)[0], '..', 'downloads')

def receive_file(port: str, file_name: str):
    rx = serial.Serial(port)

    # starting the transference by seending a NAK byte
    rx.write(NAK)
    print("Sending NAK to TX\n")

    packet = Packet()

    # waiting for a SOH
    received_line = rx.read(1)
    print("Receiving line from TX\n")

    # creating a new empty file to receive the content  
    open(os.path.join(DESTINATION_DIR, file_name),
        mode='w',
        encoding='ASCII'
    ).close()
    
    while received_line != EOT:
        print("="*55)
        print("Starting to receive a packet\n")

        # checking whether the character received was a SOH
        if received_line == SOH:
            try:
                print("\tGot a SOH char")

                # reading the package number
                packet_number = rx.read(1)
                print(f"\tPacket sequece_number: {packet_number}")

                # reading the package number compliment
                packet_number_compliment = rx.read(1)
                print("\tPacket packet_number_compliment: "+
                    f"{packet_number_compliment}")

                # reading the package data
                data = rx.read(128)

                # reading the checksum
                checksum = rx.read(1)
                print(f"\tPacket checksum: {checksum}")
            
            except UnicodeDecodeError as ue:
                print(ue)
                rx.write(CAN)

            # instantiating a new package to validate the received package
            packet.packet_number = int.from_bytes(packet_number, 'big')
            packet.data = data.decode()
            packet.set_packet_number_compliment()
            packet.set_checksum()

            # checking whether the package number compliment calculated
            # is different from the received one
            if packet_number_compliment != packet.packet_number_compliment:
                print("\tThe packet compliment number received "+
                    f"({packet_number_compliment}) doesn't match the "+
                    f" calculated one ({packet.packet_number_compliment})")
                
                # sending a CAN char in case the compliments are different
                rx.write(CAN)
            
            # checking whether the package checksum calculated
            # is equals to the received one
            if checksum == packet.checksum:
                print("\tChecksum validated!")

                # sending an ACK char to confirm the package validation
                rx.write(ACK)
                
                # writing the received data to a new file
                with open(os.path.join(DESTINATION_DIR, file_name),
                    mode='a+',
                    encoding='ASCII'
                ) as writer:
                    print("\tWriting the packet to the file")
                    writer.write(packet.data.decode())

            else:
                print(f"\tInvalid Checksum! {checksum} != {packet.checksum}")
                rx.write(NAK)

        print("\nPacket successfully received\n")
        print("="*55)

        # waiting for a SOH or an EOT char
        received_line = rx.read(1)
    
    # # sending a ACK char to TX
    rx.write(ACK)


if __name__ == '__main__':
    port_number = input("Type the port number: ")
    port = DEFAULT_PORT_PATH+port_number

    file_name = input("Type the file name: ")
    receive_file(port, file_name)


