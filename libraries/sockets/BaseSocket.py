import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR

from ..constants.constants import TYPE_ERROR_MESAGE

from abc import ABC, abstractmethod

STANDARD_LOG_MESSAGE = "Port {port}: {msg}"

class BaseSocket(ABC):

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
            raise TypeError(TYPE_ERROR_MESAGE.format(param='host', tp='str',
                inst=str(type(host))))
    
    @property
    def port(self):
        return self.__port
    
    @port.setter
    def port(self, port):
        if isinstance(port, int):
            self.__port = port        
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='port', tp='int',
                inst=str(type(port))))

    @property
    def connection(self):
        return self.__connection
    
    @connection.setter
    def connection(self, connection: socket.socket):
        if isinstance(connection, socket.socket):
            self.__connection = connection
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='connection', 
                tp='socket.socket', inst=str(type(connection))))

    @abstractmethod
    def connect(self, family: int=AF_INET, socket_type: int=SOCK_STREAM):
        pass

    def send_mesage(self, message: bytes):
        """ Sends the given message through the connected port

        Args:
            message (bytes): the message to be sent
        """
        self.connection.send(message)
    
    def receive_mesage(self, buffer_size: int) -> bytes:
        """ Receives a massege through the connected port

        Args:
            buffer_size (int): the max quantity of bytes to receive

        Returns:
            bytes: the message received
        """
        
        return self.connection.recv(buffer_size)

    def log_mesage(self, message: object):
        """ Logs a simple message in the console

        Args:
            message (object): the message to be logged
        """
        print(STANDARD_LOG_MESSAGE.format(port=self.port, msg=message))
    
    def shutdown_connection(self, how: int=SHUT_RDWR):
        self.connection.shutdown(how)
