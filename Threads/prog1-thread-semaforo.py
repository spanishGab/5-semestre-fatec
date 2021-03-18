import threading

# semaforo
# o argumento diz quantas regiões críticas podem entrar ao mesmo 
# tempo
s = threading.Semaphore(1)

a = 0
b = 0
c = 0
d = 0
x = 0

def fn1():
    global a, b, x
    while(True):
        a = 1
        b = 2
        s.acquire()
        x = a + b
        if x != 3: print('erro1')
#        print(x)
        s.release()

def fn2():
    global c, d, x
    while(True):
        c = 3
        d = 4
        s.acquire()
        x = c + d
        if x != 7: print('erro2')
#        print(x)
        s.release()

if __name__ == '__main__':
   t1 = threading.Thread(target=fn1)
   t2 = threading.Thread(target=fn2)
   t1.start()
   t2.start()
   t1.join()
   t2.join()
