from .BaseSocket import BaseSocket

import socket
from socket import AF_INET, SOCK_STREAM

class Server(BaseSocket):

    def __init__(self, host: str='127.0.0.1', port: int=5000):
        super().__init__(host, port)
    
    def connect(self,
                family: int=AF_INET, 
                socket_type: int=SOCK_STREAM,
                listen: int=1):
        if not isinstance(family, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='family', tp='int',
                inst=str(type(family))))
        
        if not isinstance(socket_type, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_type', tp='int',
                inst=str(type(socket_type))))
        
        if not isinstance(listen, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='listen', tp='int',
                inst=str(type(listen))))

        try:
            tcp = socket.socket(family=family, type=socket_type)
            tcp.bind((self.host, self.port))
            tcp.listen(listen)

        except ValueError:
            raise ValueError("The given 'socket_type' is not a valid socket type")

        self.connection, _ = tcp.accept()
