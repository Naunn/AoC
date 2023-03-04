from aocd import get_data
import yaml
import numpy as np
import re
import copy


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_five = get_data(session=S, day=5, year=2021)

# rozbicie na kolejne wiersze
sep = [row for row in re.split("\n",day_five)]

# rozbicie kolejnych wierszy na wspolrzedne
cord = [re.split(',| -> ',sep[i]) for i in range(0,len(sep))]

# pusta macierz
matrix = [[0]*1000]*1000

# cord_tst = [[0,9,5,9],
#             [8,0,0,8],
#             [9,4,3,4],
#             [2,2,2,1],
#             [7,0,7,4],
#             [6,4,2,0],
#             [0,9,2,9],
#             [3,4,1,4],
#             [0,0,8,8],
#             [5,5,8,2]]

# matrix_tst = [[0]*10]*10

# tworzenie macierzy z zawartymi sciezkami
def vert_path(matrix: list, cords: list):
    m = np.array(copy.deepcopy(matrix))
    for cord in cords:
        x1 = int(cord[0])
        y1 = int(cord[1])
        x2 = int(cord[2])
        y2 = int(cord[3])
        if x1 == x2 and y1 <= y2:
            for i in range(y1,y2+1):
                m[i][x1] += 1
        if x1 == x2 and y1 >= y2:
            for i in range(y1,y2-1,-1):
                m[i][x1] += 1
        if y1 == y2 and x1 <= x2:
            for j in range(x1,x2+1):
                m[y1][j] += 1
        if y1 == y2 and x1 >= x2:
            for j in range(x1,x2-1,-1):
                m[y1][j] += 1
    return m
# vert_path(matrix_tst, cord_tst)

print("Number of at least two lines overlap:",np.count_nonzero(vert_path(matrix, cord) > 1))

def diagonal_path(matrix: list, cords: list):
    m = np.array(copy.deepcopy(matrix))
    for cord in cords:
        x1 = int(cord[0])
        y1 = int(cord[1])
        x2 = int(cord[2])
        y2 = int(cord[3])
        if x1 == x2 and y1 < y2:
            for i in range(y1,y2+1):
                m[i][x1] += 1
        if x1 == x2 and y1 > y2:
            for i in range(y1,y2-1,-1):
                m[i][x1] += 1
        if y1 == y2 and x1 <= x2:
            for j in range(x1,x2+1):
                m[y1][j] += 1
        if y1 == y2 and x1 > x2:
            for j in range(x1,x2-1,-1):
                m[y1][j] += 1                
        if x1 > x2 and y1 < y2:
            x = [x for x in range(x1,x2-1,-1)]
            y = [y for y in range(y1,y2+1)]
            for i,j in zip(x,y):
                m[j][i] += 1
        
        if x1 < x2 and y1 > y2:
            x = [x for x in range(x1,x2+1)]
            y = [y for y in range(y1,y2-1,-1)]
            for i,j in zip(x,y):
                m[j][i] += 1
                
        if x1 > x2 and y1 > y2:
            x = [x for x in range(x1,x2-1,-1)]
            y = [y for y in range(y1,y2-1,-1)]
            for i,j in zip(x,y):
                m[j][i] += 1
        
        if x1 < x2 and y1 < y2:
            x = [x for x in range(x1,x2+1)]
            y = [y for y in range(y1,y2+1)]
            for i,j in zip(x,y):
                m[j][i] += 1
                
    return m
# diagonal_path(matrix_tst, cord_tst)

print("Number of at least two lines overlap:",np.count_nonzero(diagonal_path(matrix, cord) > 1))
