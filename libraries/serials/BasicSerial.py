import serial

from ..constants.constants import TYPE_ERROR_MESAGE, ACK, NAK, CAN, SOH, EOT

LOG_MESAGE = "{alias}: {msg}"

class BasicSerial:

    def __init__(self, alias: str, port: str):
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
        return self.__connection
    
    @connection.setter
    def connection(self, connection: serial.Serial):
        if isinstance(connection, serial.Serial):
            self.__connection = connection
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='connection', 
                tp='serial.Serial', inst=str(type(connection))))

    
    def connect(self):
        """Connects the  serial instance to the port attribute"""
        self.__connection = serial.Serial(self.port)
    
    def send_mesage(self, mesage: bytes):
        """ Sends a bytes (ASCII only) mesage

        Args:
            mesage (bytes): the mesage to be sent
        """
        self.connection.write(mesage)
    
    def receive_mesage(self, 
                       buffer_size: int=1, 
                       read_line: bool=False, 
                       read_all: bool=False) -> bytes:
        """ Receives a mesage based on the given buffer_size

        Args:
            buffer_size (int, optional): the max  mesage length to be received. Defaults to 1.
            read_line (bool, optional): if true, the mesage will be recognized by a '\n'char. 
                Defaults to False.
            read_all (bool, optional): if true, all the buffer conten will be read. 
                Defaults to False.

        Returns:
            bytes: the received mesage
        """
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
    
    def request_transference_start(self):
        self.log_mesage("Starting transference")
        self.send_mesage(SOH)
    
    def wait_transference_start(self):
        start = self.receive_mesage(1)

        if start == SOH:
            self.log_mesage("Received transference start request")
            self.log_mesage("Starting transference")
            self.send_mesage(ACK)
        else:
            self.log_mesage("Error!, invalid byte received: '"+start.decode()+"'")
            self.send_mesage(NAK)
    
    def receive_confirmation(self) -> bytes:
        confirm = self.receive_mesage(1)
        
        if confirm == ACK:
            self.log_mesage("Confirmation received")
        elif confirm == CAN:
            self.log_mesage("Canceling mesage received")
        elif confirm == NAK:
            self.log_mesage("No confirmation received")
        else:
            self.log_mesage("Error!, invalid byte received: '"+confirm.decode()+"'")

        return confirm
    
    def inform_end_of_transference(self):
        self.log_mesage("Finishing transference")
        self.send_mesage(EOT)
    
    def wait_end_of_transference(self):
        end = self.receive_mesage(1)

        if end == EOT:
            self.log_mesage("Received transference end request")
            self.log_mesage("Transference successfully finished")
            self.send_mesage(ACK)
        else:
            self.log_mesage("Error!, invalid byte received: '"+end.decode()+"'")
            self.send_mesage(NAK)

        
