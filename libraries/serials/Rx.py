import serial
from .BaseSerial import BaseSerial

RX_LOG_MESAGE "RX {alias}: {msg}"

class Rx(BaseSerial):

    def __init__(self, alias: str, port: str):
        super().__init__(port)

        self.alias = alias
    
    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, alias: str):
        if isinstance(alias, str):
            self.__alias = alias
        else:
            raise (TYPE_ERROR_MESAGE.format(param='alias', tp='str',
                inst=str(type(alias))))
    
    def log_mesage(self,  mesage: str):
        print(RX_LOG_MESAGE.format(alias=self.alias, msg=mesage))
        
