import serial
from .BasicSerial import BasicSerial
from ..constants.constants import TYPE_ERROR_MESAGE

RX_LOG_MESAGE "TX {alias}: {msg}"

class Tx(BasicSerial):

    def __init__(self, alias: str, port: str, signal: int=None):
        super().__init__(alias, port)

        self.signal = signal
    
    @property
    def signal(self):
        return self.__signal
    
    @signal.setter
    def signal(self, signal: int):
        if signal is None:
            self.__signal = signal
        elif isinstance(signal, int):
            self.__signal = signal
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='signal', tp='int',
                inst=str(type(signal))))
    
    def log_mesage(self,  mesage: str):
        print(RX_LOG_MESAGE.format(alias=self.alias, msg=mesage))

