from QuadraticFunc import QuadraticFunc

if __name__ == '__main__':
    fn = QuadraticFunc(a=1, b=-5, c=6)
    fn.build_points()
    fn.write_results()
