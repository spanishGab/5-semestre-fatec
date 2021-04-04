from constants import *

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.constants.constants import TYPE_ERROR_MESAGE

class PartnerClient:

    def __init__(self):
        self.not_using_server = True
        self.__connections = {}

    @property
    def not_using_server(self):
        return self.__not_using_server
    
    @not_using_server.setter
    def not_using_server(self, not_using_server: bool):
        if isinstance(not_using_server, bool):
            self.__not_using_server = not_using_server
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='not_using_server',
                tp='bool', inst=str(type(not_using_server))))

    def can_access_server(self):
        if not isinstance(requester_host, str):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='requester_host',
                tp='str', inst=str(type(requester_host))))

        if not isinstance(requester_port, int):
            raise TypeError(TYPE_ERROR_MESAGE.format(param='requester_port', 
                tp='int', inst=str(type(requester_port))))

        return self.not_using_server
