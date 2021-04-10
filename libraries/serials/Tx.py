import serial
from .BasicSerial import BasicSerial

RX_LOG_MESAGE "TX {alias}: {msg}"

class Tx(BasicSerial):

    def __init__(self, alias: str, port: str):
        super().__init__(alias, port)
    
    def log_mesage(self,  mesage: str):
        print(RX_LOG_MESAGE.format(alias=self.alias, msg=mesage))

