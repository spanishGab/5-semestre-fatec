import serial
from .BasicSerial import BasicSerial

RX_LOG_MESAGE = "RX {alias}: {msg}"

class Rx(BasicSerial):

    def __init__(self, alias: str, port: str, address: str=None):
        super().__init__(alias, port)

        self.address = address
    
    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, address: str):
        if address is None:
            self.__address = address
        elif isinstance(address, str):
            self.__address = address
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='address', 
                tp='str', inst=str(type(address))))
    
    def log_mesage(self,  mesage: str):
        print(RX_LOG_MESAGE.format(alias=self.alias, msg=mesage))
