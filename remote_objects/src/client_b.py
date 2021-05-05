import Pyro5.api
from random import uniform
import time

number_sum = Pyro5.api.Proxy("PYRONAME:number.sum")    # use name server object lookup uri shortcut

while True:
    #time.sleep(round(uniform(0.5, 0.7), 1))
    print(number_sum.sum_numbers('client_b', 3, 4))
    
