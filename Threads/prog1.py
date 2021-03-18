a = 0
b = 0
c = 0
d = 0
x = 0

def fn1():
    global a, b, x
    a = 1
    b = 2
    x = a + b
    print(x)

def fn2():
    global c, d, x
    c = 3
    d = 4
    x = c + d
    print(x)

if __name__ == '__main__':
    fn1()
    fn2()
