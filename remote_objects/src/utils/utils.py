HALF_LINE = [' ' for _ in range(0, 34)]
X_AXIS_LINE = '----------------------------------|---------------------------------'
X_AXIS_NUMBERS = '  -1 -2 -3 -4 -5 -6 -7 -8 -9 -10  |  1  2  3  4  5  6  7  8  9  10  '

def generate_cartesian_plane():
    cartesian_matrix = []

    for i in range(5, 0, -1):
        cartesian_matrix.append(HALF_LINE + [f'|{i}'] + HALF_LINE)
        cartesian_matrix.append(HALF_LINE + [f'|'] + HALF_LINE)
    
    cartesian_matrix.append([X_AXIS_LINE])
    cartesian_matrix.append([X_AXIS_NUMBERS])

    for i in range(-1, -6, -1):
        cartesian_matrix.append(HALF_LINE + [f'|{i}'] + HALF_LINE)
        cartesian_matrix.append(HALF_LINE + [f'|'] + HALF_LINE)
    
    return cartesian_matrix


m = generate_cartesian_plane()

for i in range(0, len(m)):
    for j in range(0, len(m[i])):
        print(m[i][j], end='')
    print('')
