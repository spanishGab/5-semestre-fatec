import os
from serial import Serial
from serial.serialutil import SerialException

USER_HOME_PATH = os.environ["HOME"] if os.environ["HOME"] is not None else "~"
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


class TX(object):
    def __init__(self, port):
        super().__init__()
        self.tx = Serial(port)
        self.user_home_path = os.path.expanduser(USER_HOME_PATH)
        self.origin_transfer_path = None

    def send_file(self, origin_transfer_path: str):
        name = None
        path = origin_transfer_path.split("/")
        try:
            self.tx.write("{0}{1}".format(START_TRANSFER_MSG, TRAILING_NEW_LINE).encode())
            confirmation_to_send = self.tx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)
            print(confirmation_to_send)

            if confirmation_to_send == CONFIRMATION_TO_SEND_MSG:
                self.origin_transfer_path = os.path.join(self.user_home_path, *path)

                with open(self.origin_transfer_path, 'r') as reader:
                    name = os.path.basename(self.origin_transfer_path)
                    self.tx.write("{0}{1}".format(name, TRAILING_NEW_LINE).encode())
                    print("file name: {0}".format(name) )

                    for line in reader.readlines():
                        if TRAILING_NEW_LINE not in line:
                            self.tx.write("{0}{1}".format(line, TRAILING_NEW_LINE).encode())
                        else:
                            self.tx.write(line.encode())
                reader.close()

                self.tx.write("{0}{1}".format(END_OF_FILE, TRAILING_NEW_LINE).encode())
                confirmation_received_file = self.tx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)
                print("RX confirmation: {0}".format(confirmation_received_file))

                if confirmation_received_file == CONFIRMATION_FILE_RECEIVED_MSG:
                    print("transferencia de arquivo finalizada")
                else:
                    print(FAIL_TO_TRANSFER_MSG)
            else:
                print(UNABLE_TO_RECEIVED_FILE_MSG)

        except Exception as e:
            print("Unable to send file to transfer with error: {0}".format(str(e)))
            raise e
        except SerialException as sex:
            print("Unable to send file to transfer with error: {0}".format(str(sex)))
            raise sex


if __name__ == "__main__":
    tx_port = input("Type the TX port: ")
    file_path = input("Type the file path based on your home directory: ")
    COMPLET_PORT = "{0}{1}".format(BASE_PORT_PATH, tx_port)
    TX(COMPLET_PORT).send_file(file_path)
