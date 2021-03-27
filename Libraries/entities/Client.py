import socket
from socket import AF_INET, SOCK_STREAM

from SocketConnectionInterface import SocketConnectionInterface

class Client(SocketConnectionInterface):

    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port

    def connect():
        self.__conn = socket.socket(family=AF_INET, type=SOCK_STREAM)


