from common_constants import SOH

class Packet:
    
    def __init__(self, pack_number: int=None, data: str=None):
        self.pack_number = pack_number
        self.data = data

    @property
    def soh(self):
        return SOH
    
    @property
    def pack_number(self):
        return self.__pack_number

    @pack_number.setter
    def pack_number(self, pack_number):
        if pack_number is None:
            self.__pack_number = None
        elif isinstance(pack_number, int):
            self.__pack_number = bytes([pack_number % 8])
        else:
            raise ValueError("The 'pack_number' param must be an instance of the "+
                "int class, got"+str(type(pack_number)))
    
    @property
    def pack_number_compliment(self):
        return self.__pack_number_compliment
    
    def set_pack_number_compliment(self):
        pack_number_compliment = int.from_bytes(self.pack_number, 'big')
        
        pack_number_compliment = ~pack_number_compliment
        
        self.__pack_number_compliment = bytes(
            [pack_number_compliment & 0xff]
        )

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        if data is None:
            self.__data = None
        elif isinstance(data, str):
            if len(data) < 128:
                data += '#'*(128 - len(data))

            self.__data = data.encode()
        else:
            raise ValueError("The 'data' param must be an instance of the str class, "+
                "got "+str(type(data)))

    @property
    def checksum(self):
        return self.__checksum
    
    def set_checksum(self):
        self.__checksum = 0
        for c in self.data.decode():
            self.__checksum += ord(c)

        self.__checksum %= 256




