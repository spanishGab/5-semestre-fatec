import os
import time
CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))
COMMON_DIR = os.path.join(CURRENT_DIR, '..', 'common')

import threading
mutex = threading.Lock()

current_int = []
next_int = 0
next_components = []
exec_order = 'r'

class NumberTranslatorMutex:

    NUMBERS = (
        'zero', 
        'one', 
        'two', 
        'three', 
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine',
    )

    def __init__(self):
        with open(os.path.join(COMMON_DIR, 'mean.txt'), 'w') as f:
            f.write('zero\n')

    def read_number(self):
        global next_int, next_components, current_int
        global exec_order

        count = 0
        
        try:
            while count < 10000:
                while exec_order == 'w': continue

                mutex.acquire()
                with open(os.path.join(COMMON_DIR, 'mean.txt'), 
                    'r', 
                    encoding='UTF-8'
                ) as f:
                    for line in f:
                        number = line

                current_components = []
                next_components = []
                
                number = number.replace('\n', '')

                for n in number.split(', '):
                    current_components.append(str(self.NUMBERS.index(n)))
                
                current_int = int(''.join(current_components))
                
                next_int = current_int+1
                
                for number in str(next_int):
                    next_components.append(self.NUMBERS[int(number)])
                
                exec_order = 'w'
                mutex.release()

                count +=1
        except Exception as e:
            print(e)

    
    def write_number(self):
        global next_int, next_components, current_int
        # time.sleep(0.001)
        global exec_order

        count = 0
        
        try:
            while count < 10000:
                while exec_order == 'r': continue
                mutex.acquire()

                with open(os.path.join(COMMON_DIR, 'mean.txt'), 
                    'a+', 
                    encoding='UTF-8'
                ) as f:
                    f.write(str(current_int)+'\n')
                    f.write(', '.join(next_components)+'\n')
                
                exec_order = 'w'
                mutex.release()

                count += 1
        except Exception as e:
            print(e)

