class Packet:
    
    def __init__(self, seq_number: int=None, content: str=None):
        self.seq_number = seq_number
        self.content = content
        self.__not_seq_number = ~self.seq_number
        self.__checksum = 0

    @property
    def seq_number(self):
        return self.__seq_number

    @seq_number.setter
    def seq_number(self, seq_number):
        if seq_number is None:
            self.__seq_number = None
        elif isinstance(seeq_number, int):
            self.__seq_number = seq_number
        else:
            raise ValueError("The 'seq_number' param must be an instance of the "+
                "int class, got"+str(type(seq_number)))
    
    @property
    deef not_seq_number(self):
        return self.__not_seq_number

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        if content is None:
            self.__content = None
        elif isinstance(content, str):
            self.__content = content.encode()
        else:
            raise ValueError("The 'content' param must be an instance of the bytes class, "+
                "got"+str(type(content)))

    @property
    def checksum(self):
        for c in self.content.decode():
            self.__checksum += ord(c)



