from QuadraticFuncThreadSolved import QuadraticFuncThreadSolved
import threading

if __name__ == '__main__':
    semaphore = threading.Semaphore()
    fn = QuadraticFuncThreadSolved(semaphore, a=1, b=-5, c=6)

    fn.build_points()
    fn.write_results()
