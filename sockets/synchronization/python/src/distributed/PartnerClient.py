from constants import *

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Client import Client
from libraries.sockets.Server import Server

from libraries.constants.constants import TYPE_ERROR_MESAGE

class PartnerClient:

    def __init__(slef):
        self.server_in_use = False

    @property
    def connections(self):
        return self.__connections
    
    def add_connection(self, 
                       connection_type: str,
                       connection_alias: str, 
                       host: str='127.0.0.1', 
                       port: int=5000):
        if isinstance(connection_alias, str):
            if connection_type.lower() == 'server':
                self.__connections[connection_alias] = Server(host, port)
                self.__connections[connection_alias].connect()
            elif connection_type.lower() == 'client':
                self.__connections[connection_alias] = Client(host, port)
                self.__connections[connection_alias].connect()
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='connection_alias',
                inst=str(type(connection_alias))))

    @property
    def server_in_use(self):
        return self.__server_in_use
    
    @server_in_use.setter
    def server_in_use(self, server_in_use: bool):
        if isinstance(server_in_use, bool):
            self.__server_in_use = server_in_use
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='server_in_use',
                tp='bool', inst=str(type(server_in_use))))

    def can_access_server(self):
        if not isinstance(requester_host, str):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='requester_host',
                tp='str', inst=str(type(requester_host))))

        if not isinstance(requester_port, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='requester_port', 
                tp='int', inst=str(type(requester_port))))

        return self.server_in_use
