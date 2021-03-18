import re
from serial import Serial
from serial.serialutil import SerialException
from threading import Thread

BASE_PORT_PATH = "/dev/pts/"
START_TRANSFER_MSG = "iniciando operacoes aritmeticas"
CONFIRMATION_TO_SEND_MSG = "apto a realizar operacao"
CONFIRMATION_RECEIVED_MSG = "operacoes recebidas com sucesso!"
OPERATIONS_FINISHED_MSG = "operacoes finalizadas"
TRAILING_NEW_LINE = "\n"
BLANK_STR = ""
FAIL_TO_TRANSFER_MSG = "falha ao enviar operandos"
UNABLE_TO_RECEIVED_FILE_MSG = "inapto a enviar operandos"
OPERATIONS_RECEIVED_SUCCESSFULLY = "operacoes matematicas realizadas com sucesso:"
SPLIT_PATTERN = "\:"
OPERANDS_TUPLE = ("+", "-", "*", "/")


class TX(object):
    def __init__(self, port, send_times):
        super().__init__()
        self.tx = Serial(port)
        self.send_times = int(send_times)

    def send_calculations(self):
        operations_finished = None
        try:
            self.tx.write("{0}{1}".format(START_TRANSFER_MSG, TRAILING_NEW_LINE).encode())
            confirmation_to_send = self.tx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)

            if confirmation_to_send == CONFIRMATION_TO_SEND_MSG:
                self.tx.write("{0}{1}".format(self.send_times, TRAILING_NEW_LINE).encode())

                for i in range(self.send_times):
                    first_operand = input("Type the first operand: ")
                    operation = input("Type arithmetic operation: ")
                    second_operand = input("Type the second operand: ")

                    self.tx.write("{0}{1}".format(first_operand, TRAILING_NEW_LINE).encode())
                    self.tx.write("{0}{1}".format(second_operand, TRAILING_NEW_LINE).encode())
                    self.tx.write("{0}{1}".format(operation, TRAILING_NEW_LINE).encode())

                    print("Operations sended: [{0}]".format(i))

                results = self.tx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)

                if "+" and "-" and "*" and "/" not in results:
                    print("{0} {1}".format(OPERATIONS_RECEIVED_SUCCESSFULLY, results))
                else:
                    operands_errors = []
                    errors = re.split(SPLIT_PATTERN, results)
                    for err in range(len(errors)):
                        x = errors[err].replace('[', '').replace(']', '').replace('\'', '')
                        if x in OPERANDS_TUPLE:
                            operands_errors.append("{0}: {1}".format(
                                x, errors[err+1].replace('[', '').replace(']', '').replace('\'', '')))
                    print(operands_errors)

                self.tx.write("{0}{1}".format(CONFIRMATION_RECEIVED_MSG, TRAILING_NEW_LINE).encode())
                operations_finished = self.tx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)

                if operations_finished == OPERATIONS_FINISHED_MSG:
                    print(operations_finished)
                else:
                    print(FAIL_TO_TRANSFER_MSG)
            else:
                print(UNABLE_TO_RECEIVED_FILE_MSG)

        except Exception as e:
            print("Unable to send operands to calculate with error: {0}".format(operations_finished))
            raise e
        except SerialException as sex:
            print("Unable to send operations to calculate with serial error: {0}".format(str(sex)))
            raise sex


if __name__ == "__main__":
    tx_port = input("Type the TX port: ")
    send_times = input("Type the quantity of operations to be executed: ")

    COMPLET_PORT = "{0}{1}".format(BASE_PORT_PATH, tx_port)

    tx = TX(COMPLET_PORT, send_times)
    calculation_job = Thread(target=tx.send_calculations)
    calculation_job.start()
    calculation_job.join()
