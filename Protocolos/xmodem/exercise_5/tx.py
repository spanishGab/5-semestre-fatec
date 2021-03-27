from os import environ
from os.path import join, expanduser
from xmodem import XMODEM
from serial import Serial
from serial.serialutil import SerialException

USER_HOME_PATH = environ["HOME"] if environ["HOME"] is not None else "~"
BASE_PORT_PATH = "/dev/pts/"
FILE_FOLDER_PATH = "/Documentos"
START_TRANSFER_MSG = "iniciando transferencia"
CONFIRMATION_TO_SEND_MSG = "apto a receber"
CONFIRMATION_FILE_RECEIVED_MSG = "arquivo recebido e copiado com sucesso"
UNABLE_TO_RECEIVED_FILE_MSG = "inapto a realizar transferencia"
TRAILING_NEW_LINE = "\n"
END_OF_FILE = "TX__EOF__RX"
BLANK_STR = ""
FAIL_TO_TRANSFER_MSG = "falha ao transferir o arquivo"

class Base(object):
    def __init__(self, serial: Serial):
        super().__init__()
        self.serial = serial
    
    def getc(self, size, timeout=1):
        return self.serial.read(size) or None

    def putc(self, data, timeout=1):
        return self.serial.write(data) or None

class TX(Base):
    def __init__(self, port):
        self.tx = Serial(port)
        self.user_home_path = expanduser(USER_HOME_PATH)
        self.origin_transfer_path = None
        self.modem = None
        super().__init__(self.tx)

    def send_file(self, origin_transfer_path: str):
        path = origin_transfer_path.split("/")
        self.modem = XMODEM(self.getc, self.putc)
        try:            
            self.origin_transfer_path = join(self.user_home_path, *path)
            print("Enviando arquivo para o caminho: {0}".format(self.origin_transfer_path))

            stream_file = open(self.origin_transfer_path, 'rb')
            result = self.modem.send(stream_file)

            print("Arquivo enviado por TX: {0}".format(result))
        except Exception as e:
            print("Erro ao enviar arquivo com XMODEM. Erro: {0}".format(str(e)))
            raise e
        except SerialException as sex:
            print("Erro ao conectar com a porta Serial. Erro: {0}".format(str(sex)))
            raise sex


if __name__ == "__main__":
    tx_port = input("Type the TX port: ")
    file_path = input("Type the file path based on your home directory: ")
    COMPLET_PORT = "{0}{1}".format(BASE_PORT_PATH, tx_port)
    TX(COMPLET_PORT).send_file(file_path)
