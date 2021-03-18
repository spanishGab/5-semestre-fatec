from threading import Thread
from NumberTranslatorSD import NumberTranslatorSD

if __name__ == '__main__':
    t = NumberTranslatorSD()
    t1 = Thread(target=t.read_number)
    t2 = Thread(target=t.write_number)

    t1.start()
    t2.start()
    t1.join()
    t2.join()
