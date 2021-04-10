import os
CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))
from collections import namedtuple

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

class QuadraticFunc():

    def __init__(self, **kwargs):
        global a, b, c
        
        a = kwargs['a']
        b = kwargs['b']
        c = kwargs['c']

    def calculate_points(self, x):
        global a, b, c, x_points, y_points

        for i in range(0, 100000):
            y_points.append(a * (x+i)**2 + b * (x+i) + c)
            y_points.append(a * (x-i)**2 + b * (x-i) + c)
            
            x_points.append((x+i))
            x_points.append((x-i))
    
    def build_points(self):
        global Points, points
        global x1, x2, x_points, y_points

        delta =  b**2 - 4 * a * c

        x1 = (-b + delta)/ 2*a
        x2 = (-b - delta)/ 2*a

        self.calculate_points(x1)
        self.calculate_points(x2)

        points = Points(x=x_points, y=y_points)
        del x_points, y_points

    @staticmethod
    def write_results():
        global points

        with open(os.path.join(CURRENT_DIR, '..', 'out', 'quadratic.txt'), 'w') as f:
            f.write(f"The funtion has the following roots: x1 = {x1}, x2 = {x2}")
            f.write("\n\nSome of its parabola's points:\n")

            points = set(zip(points.x, points.y))

            for point in sorted(points):
                f.write(f"\t[{point[0]}, {point[1]}]\n")

    