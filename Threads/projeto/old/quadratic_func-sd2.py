import threading
from QuadraticFunc import QuadraticFunc

if __name__ == '__main__':
    fn = QuadraticFunc(a=1, b=-5, c=6)
    t1 = threading.Thread(target=fn.build_points)
    t2 = threading.Thread(target=fn.write_results)
    t1.start()
    t2.start()
    t1.join()
    t2.join()    
