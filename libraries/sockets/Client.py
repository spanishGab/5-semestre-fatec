from .BaseSocket import BaseSocket

import socket
from socket import AF_INET, SOCK_STREAM

from ..constants.constants import TYPE_ERROR_MESAGE

STANDARD_LOG_MESSAGE = "Client {cli}: {msg}"

class Client(BaseSocket):

    def __init__(self, 
                 alias: str='client', 
                 host: str='127.0.0.1', 
                 port: int=5000):
        super().__init__(alias, host, port)
    
    def connect(self, 
                family: int=AF_INET, 
                socket_type: int=SOCK_STREAM, 
                listen=None,
                protocol: int=-1):
        if not isinstance(family, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='family', tp='int',
                inst=str(type(family))))
        
        if not isinstance(socket_type, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_type', tp='int',
                inst=str(type(socket_type))))

        try:
            self.connection = socket.socket(family=family, type=socket_type, proto=protocol)
        except ValueError:
            raise ValueError("The given 'socket_type' is not a valid socket type")

        self.connection.connect((self.host, self.port))
