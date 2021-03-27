from common_constants import SOH

class Packet:
    
    def __init__(self, packet_number: int=None, data: str=None):
        self.packet_number = packet_number
        self.data = data

    @property
    def soh(self):
        return SOH
    
    @property
    def packet_number(self):
        return self.__packet_number

    @packet_number.setter
    def packet_number(self, packet_number):
        if packet_number is None:
            self.__packet_number = None
        elif isinstance(packet_number, int):
            self.__packet_number = bytes([packet_number])
        else:
            raise ValueError("The 'packet_number' param must be an instance of the "+
                "int class, got"+str(type(packet_number)))
    
    @property
    def packet_number_compliment(self):
        return self.__packet_number_compliment
    
    def set_packet_number_compliment(self):
        packet_number_compliment = int.from_bytes(self.packet_number, 'big')
        
        packet_number_compliment = ~packet_number_compliment
        
        self.__packet_number_compliment = bytes(
            [packet_number_compliment & 0xff]
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
        checksum = 0
        for c in self.data.decode():
            checksum += ord(c)

        self.__checksum = bytes(
            [checksum & 0xff]
        )




