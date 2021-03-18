from serial import Serial
from serial.serialutil import SerialException

BASE_PORT_PATH = "/dev/pts/"
START_TRANSFER_MSG = "iniciando operacoes aritmeticas"
CONFIRMATION_TO_SEND_MSG = "apto a realizar operacao"
CONFIRMATION_RECEIVED_MSG = "operacoes recebidas com sucesso!"
OPERATIONS_FINISHED_MSG = "operacoes finalizadas"
TRAILING_NEW_LINE = "\n"
BLANK_STR = ""
RESULT_MSG = "resultado: []"
FAIL_TO_RECEIVE_CONFIRMATION_MSG = "falha ao receber mensagem de confirmacao"
UNABLE_TO_SEND_CALCULATIONS_MSG = "inapto a enviar calculos"



class RX(object):
    def __init__(self, port):
        super().__init__()
        self.rx = Serial(port)
        self.calculations_count = 0

    def execute_calculations(self):
        results = []
        result = None
        try:
            confirmation_to_calculate = self.rx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)

            if confirmation_to_calculate == START_TRANSFER_MSG:
                self.rx.write("{0}{1}".format(CONFIRMATION_TO_SEND_MSG, TRAILING_NEW_LINE).encode())
                self.calculations_count = int(self.rx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR))
                print("{0}. Iterations: {1}".format(confirmation_to_calculate, self.calculations_count))

                for _ in range(self.calculations_count):
                    try:
                        first_operand = self.rx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)
                        second_operand = self.rx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)
                        operation = self.rx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)
                        result = eval("{0}{1}{2}".format(first_operand, operation, second_operand))
                        results.append("{0}".format(RESULT_MSG.replace("[]", str(result))))
                        
                        print("Operation successfully executed: {0}".format(result))
                    except Exception as e:
                        results.append("{0}: {1}".format(operation, str(e)))
                        print("Unable to calculate operation {0} with error: {1}".format(operation, str(e)))
                
                self.rx.write("{0}{1}".format(str(results), TRAILING_NEW_LINE).encode())

                confirmation_received = self.rx.readline().decode().replace(TRAILING_NEW_LINE, BLANK_STR)
                if confirmation_received == CONFIRMATION_RECEIVED_MSG:
                    print(confirmation_received)
                    self.rx.write("{0}{1}".format(OPERATIONS_FINISHED_MSG, TRAILING_NEW_LINE).encode())
                else:
                    print(confirmation_received)
                    self.rx.write("{0}{1}".format(FAIL_TO_RECEIVE_CONFIRMATION_MSG, TRAILING_NEW_LINE).encode())
            else:
                print(confirmation_to_calculate)
                self.rx.write("{0}{1}".format(UNABLE_TO_SEND_CALCULATIONS_MSG, TRAILING_NEW_LINE).encode())
        except Exception as e:
            print("Unable to execute calculations with error: {0}".format(str(e)))
            raise e
        except SerialException as sex:
            print("Unable to execute calculations with serial error: {0}".format(str(sex)))
            raise sex


if __name__ == "__main__":
    rx_port = input("Type the RX port: ")
    PORT = "{0}{1}".format(BASE_PORT_PATH, rx_port)
    RX(PORT).execute_calculations()
