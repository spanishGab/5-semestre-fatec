from .BaseSocket import BaseSocket

import socket
from socket import AF_PACKET, SOCK_RAW, htons

from ..constants.constants import TYPE_ERROR_MESAGE

STANDARD_LOG_MESSAGE = "Server {srv}: {msg}"
ETHERNET_P_ALL = 3

class EthernetSocket(BaseSocket):

    def __init__(self, 
                 alias: str='ethernet',
                 interface: str='127.0.0.1', 
                 port: int=0):
        super().__init__(alias=alias, port=port)

        self.interface = interface
    
    @property
    def interface(self):
        return self.__interface
    
    @interface.setter
    def interface(self, interface):
        if isinstance(interface, str):
            self.__interface = interface        
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='interface', tp='str',
                inst=str(type(interface))))
    
    def connect(self,
                family: int=AF_PACKET, 
                socket_type: int=SOCK_RAW,
                listen: int=None,
                protocol: int=htons(ETHERNET_P_ALL)):
        if not isinstance(family, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='family', tp='int',
                inst=str(type(family))))
        
        if not isinstance(socket_type, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_type', tp='int',
                inst=str(type(socket_type))))

        try:
            self.connection = socket.socket(family=family, type=socket_type, proto=protocol)
            self.connection.bind((self.interface, self.port))
        except ValueError:
            raise ValueError("The given 'socket_type' is not a valid socket type")
    
    def send_mesage(self, message: bytes):
        """ Sends the given message through the connected port

        Args:
            message (bytes): the message to be sent
        """
        self.connection.sendall(message)
    

