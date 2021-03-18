import serial


def do_arithmetic_operation(port: str):
    rx = serial.Serial(port)
    mensagemConfirmacao = rx.readline().decode()
    if mensagemConfirmacao == "iniciando operacao\n":
        print("apto a realizar operacao\n")
    else:
        print("Nao esta apto a realizar operacao")

    first_operand = rx.readline().decode().replace('\n', '')

    operation = rx.readline().decode().replace('\n', '')

    second_operand = rx.readline().decode().replace('\n', '')

    print(first_operand+operation+second_operand)
    rx.write((str(eval(first_operand+operation+second_operand))+'\n').encode())
    rx.write(("operacao realizada com sucesso\n").encode())

    if rx.readline().decode() == 'operacao recebida\n':
        print('calculo executado com sucesso')
    else:
        print('erro ao calcular')


if __name__ == '__main__':
    rx_port = input('Type the RX port number: ')
    do_arithmetic_operation('/dev/pts/'+rx_port)
