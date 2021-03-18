import os
CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))
COMMON_DIR = os.path.join(CURRENT_DIR, '..', 'common')

current_int = []
next_int = 0
next_components = []

class NumberTranslator:

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

        with open(os.path.join(COMMON_DIR, 'mean.txt'), 'r', encoding='UTF-8') as f:
            for line in f:
                number = line
        
        number = number.replace('\n', '')

        current_components = []
        for n in number.split(', '):
            current_components.append(str(self.NUMBERS.index(n)))
        
        current_int = int(''.join(current_components))
        
        next_int = current_int+1
        next_components = []        
        
        for number in str(next_int):
            next_components.append(self.NUMBERS[int(number)])
    
    def write_number(self):
        global next_int, next_components, current_int

        with open(os.path.join(COMMON_DIR, 'mean.txt'), 'a+', encoding='UTF-8') as f:
            f.write(str(current_int)+'\n')
            f.write(', '.join(next_components)+'\n')                    
