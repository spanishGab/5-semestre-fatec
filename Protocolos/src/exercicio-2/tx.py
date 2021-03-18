import serial


def send_arithmetic_operation(port: str):
    tx = serial.Serial(port)
    tx.write(("iniciando operacao\n").encode())

    # reading the first operand
    first_operand = input("Type the first operand: ")

    # reading the operation
    operation = input("Type the arithmetic opration: ")

    # reading the second operand
    second_operand = input("Type the second operand: ")

    # sending the operation elements
    tx.write((first_operand+'\n').encode())
    tx.write((operation+'\n').encode())
    tx.write((second_operand+'\n').encode())

    # catching the operation result
    result = tx.readline().decode()
    print(result)

    if tx.readline().decode() == "operacao realizada com sucesso\n":
        tx.write("operacao recebida\n".encode())
    else:
        tx.write("operacao não recebida\n".encode())


if __name__ == '__main__':
    tx_port = input('Type the TX port number: ')
    send_arithmetic_operation('/dev/pts/'+tx_port)
