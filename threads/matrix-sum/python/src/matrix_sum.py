from threading import Thread, Semaphore
from concurrent.futures import ThreadPoolExecutor
from random import randint

semaphore = Semaphore(1)
result_matrix = []

def generate_matrix(m: int, n: int) -> list:
    matrix = []
    
    for line in range(0, m):
        matrix.append([])
        for column in range(0, n):
            matrix[line].append(randint(1, 11))
    
    return matrix


def sum_lines(line_a: list, line_b: list) -> list:
    global result_matrix
    result = []
    
    for i in range(0, len(line_a)):
        result.append(line_a[i] + line_b[i])
    
    semaphore.acquire()
    result_matrix.append(result)
    semaphore.release()


if __name__ == '__main__':
    matrix_lines = int(input("Type the matrixes' line quantity: "))
    matrix_columns = int(input("Type the matrixes' column quantity: "))

    with ThreadPoolExecutor(max_workers=2) as executor:
        mat = executor.submit(generate_matrix, matrix_lines, matrix_columns)
        matrix_a = mat.result()

        mat = executor.submit(generate_matrix, matrix_lines, matrix_columns)
        matrix_b = mat.result()
    
    print(matrix_a)
        
    print(matrix_b)

    with ThreadPoolExecutor(max_workers=matrix_lines) as executor:
        for node in range(0, matrix_lines):
            executor.submit(sum_lines, matrix_a[node], matrix_b[node])
  
    print(result_matrix)
