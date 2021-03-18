from NumberTranslator import NumberTranslator

if __name__ == '__main__':
    t = NumberTranslator()
    count = 0
    while count < 10000:
        t.read_number()
        t.write_number()
        count += 1