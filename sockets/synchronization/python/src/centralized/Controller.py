from constants import GITHUB_DIR

import sys
sys.path.insert(1, GITHUB_DIR)

from libraries.sockets.Server import Server

from libraries.constants.constants import (
    TYPE_ERROR_MESAGE, 
    ACK, 
    NAK, 
    CAN
)

import socket

class Controller():
    
    def __init__(self, max_accesses: int):
        self.__connections = {}

        self.__max_accesses = max_accesses
        self.__acquire_calls = 0
    
    @property
    def connections(self):
        return self.__connections
    
    def add_connection(self, 
                       connection_alias: str, 
                       host: str='127.0.0.1', 
                       port: int=5000):
        if isinstance(connection_alias, str):
            self.__connections[connection_alias] = Server(connection_alias, host, 
                port)
            self.__connections[connection_alias].connect()
        
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='connection_alias',
                inst=str(type(connection_alias))))

    @property
    def max_accesses(self):
        return self.__max_accesses
    
    @max_accesses.setter
    def max_accesses(self, max_accesses: int):
        if isinstance(max_accesses, int):
            if max_accesses > 0:
                self.__max_accesses = max_accesses
            else:
                raise ValueError("The 'max_accesses' param must be bigger than"+
                    " 0 (zero)")
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='max_accesses', 
                inst=str(type(max_accesses))))

    def _acquire(self, semaphore: int) -> object:
        if semaphore >= 0:
            semaphore -= 1
            self.__acquire_calls +=1
            
            return semaphore
        
        return False

    def _release(self, semaphore: int) -> object:
        release_test = semaphore
        
        if release_test == (self.max_accesses - self.__acquire_calls):
            release_test += 1
            self.__acquire_calls -= 1
            return release_test
        
        return False
    
    def request_aquire(self, conn_alias: str, semaphore: int) -> object:
        try:
            self.connections[conn_alias].log_mesage("Waiting for an NAK byte")
            request = self.connections[conn_alias].receive_mesage(1)

            if request == NAK:
                self.connections[conn_alias].log_mesage("NAK byte received")

                acquire_response = self._acquire(semaphore)

                if acquire_response is not False:
                    self.connections[conn_alias].log_mesage("Sending an ACK byte, "+
                        "acquired semaphore!")

                    self.connections[conn_alias].send_mesage(ACK)
                    return acquire_response
                else:
                    self.connections[conn_alias].log_mesage("Sending an CAN byte, "+
                        "could not acquire semaphore!")

                    self.connections[conn_alias].send_mesage(CAN)
            else:
                self.connections[conn_alias].log_mesage("NAK byte not received")
                return None
        except KeyError:
            raise KeyError("The '"+conn_alias+"' connection alias does not exist")
    
    def request_release(self, conn_alias: str, semaphore: int) -> object:
        try:
            self.connections[conn_alias].log_mesage("Waiting for an NAK byte")
            request = self.connections[conn_alias].receive_mesage(1)

            if request == NAK:
                self.connections[conn_alias].log_mesage("NAK byte received")

                release_response = self._release(semaphore)
                
                if release_response is not False:
                    self.connections[conn_alias].log_mesage("Sending an ACK byte, "+
                        "released semaphore!")

                    self.connections[conn_alias].send_mesage(ACK)
                    return release_response
                else:
                    self.connections[conn_alias].log_mesage("Sending an CAN byte, "+
                        "could not release semaphore!")

                    self.connections[conn_alias].send_mesage(CAN)
                    raise Exception("Client requested a 'release' before an 'acquire'"+
                        ", aborting!")
            else:
                self.connections[conn_alias].log_mesage("NAK byte not received")
                return None
        except KeyError:
            raise KeyError("The '"+conn_alias+"' connection alias does not exist")


