import sys
from ..constants.constants import *

sys.path.append(ROOT_DIR)

from libraries.serials.Tx import Tx
from libraries.serials.Rx import Rx
from libraries.constants.constants import ACK, CAN, NAK

TX_ALIAS = "TX_PC2"
RX_ALIAS = "RX_PC2"
RX_TX_ALIAS = "RX_TX_PC2"


def send(alias: str, 
         port: str, 
         destination_addres: str, 
         mesage: bytes=None,
         origin: str=TX_ALIAS) -> bool:
    tx = Tx(alias, port)

    tx.connect()

    tx.request_transference_start()

    confirm = tx.receive_confirmation()
    if confirm == ACK:
        tx.log_mesage("Sending the mesage to computer "+str(destination_addres))
        
        tx.send_mesage(origin.encode()+TRAILING_NEW_LINE)
        tx.send_mesage(destination_addres.encode()+TRAILING_NEW_LINE)
        tx.send_mesage(mesage+TRAILING_NEW_LINE)

        tx.wait_end_of_transference()
    elif confirm == CAN or confirm == NAK:
        tx.log_mesage("RX aborted transference")
        return False
    else:
        tx.log_mesage("Aborting transference")
        return False
    
    return True


def receive(rx_alias: str, tx_alias: str, rx_port: str, tx_port: str):
    rx = Rx(rx_alias, rx_port, rx_port)

    rx.connect()

    rx.wait_transference_start()

    origin = rx.receive_mesage(read_line=True).decode().replace('\n', '')
    destination = rx.receive_mesage(read_line=True).decode().replace('\n', '')
    mesage = rx.receive_mesage(read_line=True).replace(TRAILING_NEW_LINE, b'')

    if destination == rx.address:
        print("Computer "+origin+" says: "+mesage.decode())
    else:
        if send(tx_alias, tx_port, destination, mesage, origin):
            rx.log_mesage("Mesage forwarded to port"+destination)
        else:
            rx.log_mesage("Failed to forward mesage to port"+destination)
            rx.log_mesage("Aborting transference!")
            return None
    
    rx.inform_end_of_transference()
    
    confirm = rx.receive_confirmation()
    if confirm == ACK:
        rx.log_mesage("Transference successfully finished")
    else:
        rx.log_mesage("Transference failed, aborting")
        return None


def main():
    pc_type = input("""Type the pc type \n1 - send\n2 - receive:\n-> """)

    if pc_type == '1':
        tx_port = input("Type the TX port number: ")
        tx_port = PORT_BASE_PATH + tx_port

        destination_port = input("Type the destination computer port number: ")
        destination_port = PORT_BASE_PATH + destination_port

        mesage = input("Type mesage to be sent: ").encode()
        send(TX_ALIAS, tx_port, destination_port, mesage)
    
    elif pc_type == '2':
        rx_port = input("Type the RX port number: ")
        rx_port = PORT_BASE_PATH + rx_port
    
        rx_tx_port = input("Type the port number to the TX: ")
        rx_tx_port = PORT_BASE_PATH + rx_tx_port
        
        receive(RX_ALIAS, RX_TX_ALIAS, rx_port, rx_tx_port)
    else:
        print("Wrong type typed!")


