from common_constants import SOH

class Packet:
    
    def __init__(self, seq_number: bytes=None, data: str=None):
        self.seq_number = seq_number
        self.data = data
        self.__set_compliment_seq_number()
        self.__set_checksum()

    @property
    def soh(self):
        return SOH
    
    @property
    def seq_number(self):
        return self.__seq_number

    @seq_number.setter
    def seq_number(self, seq_number):
        if seq_number is None:
            self.__seq_number = None
        elif isinstance(seeq_number, bytes):
            self.__seq_number = seq_number
        else:
            raise ValueError("The 'seq_number' param must be an instance of the "+
                "bytes class, got"+str(type(seq_number)))
    
    @property
    def compliment_seq_number(self):
        return self.__compliment_seq_number
    
    def __set_compliment_seq_number(self):
        self.__compliment_seq_number = ''

        for bit in self.seq_number.decode():
            if bit == '1':
                self.__compliment_seq_number += '0'
            elif bit == '0':
                self.__compliment_seq_number += '1'
        
        self.__compliment_seq_number.encode()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        if data is None:
            self.__data = None
        elif isinstance(data, str):
            self.__data = data.encode()
        else:
            raise ValueError("The 'data' param must be an instance of the bytes class, "+
                "got"+str(type(data)))

    @property
    def checksum(self):
        return self.__checksum
    
    def __set_checksum(self):
        self.__checksum = 0
        for c in self.data.decode():
            self.__checksum += ord(c)

        self.__checksum %= 256




