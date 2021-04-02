import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR

from ..constants.constants import TYPE_ERROR_MESAGE

STANDARD_LOG_MESSAGE = "Port {port}: {msg}"

class BaseSocket:

    def __init__(self, host: str='127.0.0.1', port: int=5000):
        self.host = host
        self.port = port
    
    @property
    def host(self):
        return self.__host
    
    @host.setter
    def host(self, host):
        if isinstance(host, str):
            self.__host = host        
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='host', 
                inst=str(type(host))))
    
    @property
    def port(self):
        return self.__port
    
    @port.setter
    def port(self, port):
        if isinstance(port, int):
            self.__port = port        
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='port', 
                inst=str(type(port))))

    @property
    def connection(self):
        return self.__connection

    def connect(self, family: int=AF_INET, socket_type: int=SOCK_STREAM):
        if not isinstance(family, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='family', 
                inst=str(type(family))))
        
        if not isinstance(socket_type, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_type', 
                inst=str(type(socket_type))))

        try:
            tcp = socket.socket(family=AF_INET, type=SOCK_STREAM)
        except ValueError:
            raise ValueError("The given 'socket_type' is not a valid socket type")

        self.__connection = tcp.connect((host, port))
    
    def send_message(self, message: bytes):
        """ Sends the given message through the connected port

        Args:
            message (bytes): the message to be sent
        """
        self.__connection.send(message)
    
    def receive_message(self, buffer_size: int) -> bytes:
        """ Receives a massege through the connected port

        Args:
            buffer_size (int): the max quantity of bytes to receive

        Returns:
            bytes: the message received
        """
        
        return self.connection.recv(buffer_size)

    def log_message(self, message: object):
        """ Logs a simple message in the console

        Args:
            message (object): the message to be logged
        """
        print(STANDARD_LOG_MESSAGE.format(port=self.port, msg=message))


