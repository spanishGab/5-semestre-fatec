from io import TextIOWrapper
from os.path import join, expanduser, getsize
from os import environ
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


class RX(object):
    def __init__(self, port):
        super().__init__()
        self.rx = Serial(port)
        self.user_home_path = expanduser(USER_HOME_PATH)
        self.destination_transfer_path = FILE_FOLDER_PATH.split("/")

    def recieve_file(self):
        file_line = None
        file_content = []
        try:
            confirmation_to_transfer = self.rx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)

            if confirmation_to_transfer == START_TRANSFER_MSG:
                print(confirmation_to_transfer)
                self.rx.write("{0}{1}".format(CONFIRMATION_TO_SEND_MSG, TRAILING_NEW_LINE).encode())
            else:
                print(confirmation_to_transfer)
                self.rx.write("{0}{1}".format(UNABLE_TO_RECEIVED_FILE_MSG, TRAILING_NEW_LINE).encode())
                return

            file_name = self.rx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR) 
            complete_transfer_path = join(self.user_home_path, *self.destination_transfer_path)
            path = join(complete_transfer_path, file_name)

            while True:
                file_line = self.rx.readline().decode()

                if file_line == "{0}{1}".format(END_OF_FILE, TRAILING_NEW_LINE):
                        break
                file_content.append(file_line)

            with open(path, "w") as writer:
                self.__write_file(writer, file_content)

            print("Bytes writed: {0}".format(getsize(path)))    
            
            self.rx.write("{0}{1}".format(CONFIRMATION_FILE_RECEIVED_MSG, TRAILING_NEW_LINE).encode())

            print("{0} Path: {1}".format(CONFIRMATION_FILE_RECEIVED_MSG, path))
        except SerialException as sex:
            print("Unable to transfer file with error: {0}".format(str(sex)))
            self.rx.write("{0}{1}".format(FAIL_TO_TRANSFER_MSG.replace("[]", str(sex)), TRAILING_NEW_LINE).encode())
            raise sex
        except Exception as e:
            print("Unable to transfer file with error: {0}".format(str(e)))
            self.rx.write("{0}{1}".format(FAIL_TO_TRANSFER_MSG.replace("[]", str(e)), TRAILING_NEW_LINE).encode())
            raise e

    def __write_file(self, writer: TextIOWrapper, content: list):
            for line in content:
                writer.write(line)
            writer.close()

if __name__ == '__main__':
    rx_port = input('Type the RX port number: ')
    PORT = "{0}{1}".format(BASE_PORT_PATH, rx_port)
    RX(PORT).recieve_file()
