from xmodem import XMODEM
from os import environ
from os.path import join, expanduser, getsize
from serial import Serial
from serial.serialutil import SerialException

USER_HOME_PATH = environ["HOME"] if environ["HOME"] is not None else "~"
BASE_PORT_PATH = "/dev/pts/"
FILE_FOLDER_PATH = "/Documents"
START_TRANSFER_MSG = "iniciando transferencia"
CONFIRMATION_TO_SEND_MSG = "apto a receber"
CONFIRMATION_FILE_RECEIVED_MSG = "arquivo recebido e copiado com sucesso"
UNABLE_TO_RECEIVED_FILE_MSG = "inapto a realizar transferencia"
TRAILING_NEW_LINE = "\n"
END_OF_FILE = "TX__EOF__RX"
BLANK_STR = ""
FAIL_TO_TRANSFER_MSG = "erro: [] ao transferir arquivo"


class Base(object):
    def __init__(self, serial: Serial):
        super().__init__()
        self.serial = serial
    
    def getc(self, size, timeout=1):
        return self.serial.read(size) or None

    def putc(self, data, timeout=1):
        return self.serial.write(data) or None

class RX(Base):
    def __init__(self, port):
        self.rx = Serial(port)
        self.user_home_path = expanduser(USER_HOME_PATH)
        self.destination_transfer_path = FILE_FOLDER_PATH.split("/")
        self.modem = None
        super().__init__(self.rx)

    def recieve_file(self):
        self.modem = XMODEM(self.getc, self.putc)
        try:
            complete_transfer_path = join(self.user_home_path, *self.destination_transfer_path)
            print("Transferindo arquivo para o path: {0}".format(complete_transfer_path))

            stream = open(complete_transfer_path + '/test_file.txt', 'wb')
            bytes_transfered = self.modem.recv(stream)

            print("Arquivo Recebido. Total de bytes: {0}".format(bytes_transfered))

        except SerialException as sex:
            print("Erro ao conectar na porta Serial. Erro: {0}".format(str(sex)))
            self.rx.write("{0}{1}".format(FAIL_TO_TRANSFER_MSG.replace("[]", str(sex)), TRAILING_NEW_LINE).encode())
            raise sex
        except Exception as e:
            print("Erro ao receber arquivo com XMODEM. Erro: {0}".format(str(e)))
            self.rx.write("{0}{1}".format(FAIL_TO_TRANSFER_MSG.replace("[]", str(e)), TRAILING_NEW_LINE).encode())
            raise e


if __name__ == '__main__':
    rx_port = input('Type the RX port number: ')
    PORT = "{0}{1}".format(BASE_PORT_PATH, rx_port)
    RX(PORT).recieve_file()
