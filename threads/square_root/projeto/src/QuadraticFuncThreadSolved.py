import os
CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))
import threading
from collections import namedtuple
from QuadraticFunc import QuadraticFunc



a = None
b = None
c = None

delta = 0
x1 = 0
x2 = 0

x_points = []
y_points = []

Points = namedtuple('Points', ['x', 'y'])
points = Points(x='None', y='None')

class QuadraticFuncThreadSolved():

    def __init__(self, thread_solver, **kwargs):
        global a, b, c
        
        a = kwargs['a']
        b = kwargs['b']
        c = kwargs['c']
        
        self.thread_solver = thread_solver
    
    def calculate_points(self, x, x_start, x_stop):
        global a, b, c, x_points, y_points
   
        with self.thread_solver:
            for i in range(x_start, x_stop):
                y_points.append(a * (x+i)**2 + b * (x+i) + c)
                y_points.append(a * (x-i)**2 + b * (x-i) + c)
                
                x_points.append((x+i))
                x_points.append((x-i))    

    def build_points(self):
        global Points, points
        global x1, x2, x_points, y_points

        delta =  b**2 - 4 * a * c

        x1 = (-b + delta)/2*a
        x2 = (-b - delta)/2*a

        t1 = threading.Thread(target=self.calculate_points, args=(x1, 0, 50000))
        t2 = threading.Thread(target=self.calculate_points, args=(x1, 50000, 100000))

        t3 = threading.Thread(target=self.calculate_points, args=(x2, 0, 50000))
        t4 = threading.Thread(target=self.calculate_points, args=(x2, 50000, 100000))
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        
        with self.thread_solver:
            points = Points(x=x_points, y=y_points)
            del x_points, y_points
    
    def write_results(self):
        global points

        with open(os.path.join(CURRENT_DIR, '..', 'out', 'quadratic.txt'), 'w') as f:
            f.write(f"The funtion has the following roots: x1 = {x1}, x2 = {x2}")
            f.write("\n\nSome of its parabola's points:\n")

            # with self.thread_solver:
            points = set(zip(points.x, points.y))

            for point in sorted(points):
                f.write(f"\t[{point[0]}, {point[1]}]\n")

    
