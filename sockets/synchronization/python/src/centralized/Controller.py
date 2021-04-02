from constants import GITHUB_DIR

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.BaseSocket import BaseSocket

from libraries.constants.constants import TYPE_ERROR_MESAGE

class Controller():
    
    def __init__(self, semaphore: int):
        self.semaphore = semaphore
        self.__connections = {}

        self.__max_accesses = semaphore
        self.__acquire_calls = 0
    
    @property
    def connections(self):
        return self.__connections
    
    def add_connection(self, 
                       connection_alias: str, 
                       host: str='127.0.0.1', 
                       port: int=5000):
        if isinstance(connection_alias, str):
            self.__connections[connection_alias] = BaseSocket(host, port)
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='connection_alias',
                inst=str(type(connection_alias))))

    @property
    def semaphore(self):
        return self.__semaphore
    
    @semaphore.setter
    def semaphore(self, semaphore: int):
        if isinstance(semaphore, int):
            if semaphore >= 0:
                self.__semaphore = semaphore
            else:
                raise ValueError("The 'semaphore' param must be bigger than"+
                    " or equal to 0 (zero)")
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='semaphore', 
                inst=str(type(semaphore))))

    def acquire(self) -> bool:
        if self.semaphore >= 0:
            self.semaphore -= 1
            self.__acquire_calls +=1
            
            return True
        
        return False

    def release(self) -> bool:
        release_test = self.semaphore
        release_test += 1
        
        if release_test == (self.__max_accesses - self.__acquire_calls):
            self.semaphore = release_test
            return True
        
        return False
