import serial

from ..constants.constants import TYPE_ERROR_MESAGE

LOG_MESAGE = "{alias}: {msg}"

class BaseSerial:

    def __init__(self, port: str):
        self.port = port
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

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port: str):
        if isinstance(port, str):
            self.__port = port
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='port', tp='str',
                inst=str(type(port))))
    
    @property
    def connection(self):
        return __connection
    
    @connection.setter
    def connection(self, connection: serial.Serial):
        if isinstance(connection, serial.Serial):
            self.__connection = connection
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='connection', 
                tp='serial.Serial', inst=str(type(connection))))

    
    def connect(self, timeout=None, write_timeout=None):
        self.__connection = serial.Serial(self.port, timeout=timeout,
            write_timeout=write_timeout)
    
    def send_mesage(self, mesage: bytes):
        self.connection.write(mesage)
    
    def receive_mesage(self, 
                       buffer_size: int=1, 
                       read_line: bool=False, 
                       read_all: bool=False):
        mesage = None
        
        if read_all:
            mesage = self.connection.read_all()
        elif read_line:
            mesage = self.connection.readline()
        else:
            mesage = self.connection.read(buffer_size)
        
        return mesage
    
    def log_mesage(self, mesage: str):
        print(LOG_MESAGE.format(alias=self.alias, msg=mesage))        
        
