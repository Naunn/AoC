2# -*- coding: utf-8 -*-
"""
Created on Mon May 30 09:44:20 2022

@author: Bartosz Lewandowski
"""
# %% import
from aocd import get_data
S = "53616c7465645f5f14044fb9e9c8529fb52cd27efaee89e40ccc4a65b109fd6eef45152740499f22ab9faf1e9d33d299f44dabccb491f0da6643251321077c66"
import pandas as pd
import numpy as np
from statistics import mode
import copy
import re
# %% zadanie 1
day_one = get_data(session=S, day=1, year=2021)

# Przeniesienie przekonwertowanych pomiarów do listy.
# Nie mozna wrzucic w set, bo "zjada" wartosci. Z 2000 do 1639.
measurement = []
for M in day_one.split('\n'):
    measurement.append(int(M))
    
# Zliczanie increase i decrease
def incr_decr(measures: list):
    increase = 0
    decrease = 0
    for i in range(1,len(measures)):
        if measures[i] > measures[i-1]:
            increase += 1
        if measures[i] < measures[i-1]:
            decrease += 1
            
    print("increase = {} \ndecrease = {}".format(increase,decrease))
    
incr_decr(measurement)

# Zsumowanie 3 kolejnych pomiarow i zapisanie w jednej liscie
measurement_3 = []
for i in range(len(measurement)-2):
    measurement_3.append(measurement[i]+measurement[i+1]+measurement[i+2])
    
incr_decr(measurement_3)

# %% zadanie 2
day_two = get_data(session=S, day=2, year=2021)

# Slownik do zapisu polozenia
position = {"horizontal position": 0,
            "depth": 0}

# Obliczanie polozenia przez zmiany zapisow w slowniku
for M in day_two.split('\n'):
    temp = M.split(" ")
    if temp[0] == "forward":
        position["horizontal position"] += int(temp[1])
    if temp[0] == "down":
        position["depth"] += int(temp[1])
    if temp[0] == "up":
        position["depth"] -= int(temp[1])
print("horizontal*depth:",position["horizontal position"]*position["depth"])

# Slownik rozszerzony o aim
position = {"horizontal position": 0,
            "depth": 0,
            "aim": 0}

# Obliczanie polozenia przez zmiany zapisow w slowniku z uwzglednieniem aim
for M in day_two.split('\n'):
    temp = M.split(" ")
    if temp[0] == "forward":
        position["horizontal position"] += int(temp[1])
        position["depth"] += position["aim"]*int(temp[1])
    if temp[0] == "down":
        position["aim"] += int(temp[1])
    if temp[0] == "up":
        position["aim"] -= int(temp[1])
print("horizontal*depth (with aim):",position["horizontal position"]*position["depth"])

# %% zadanie 3
day_three = get_data(session=S, day=3, year=2021)

df = pd.DataFrame([list(M) for M in day_three.split("\n")])

# Wykorzystanie desc() do wyciagniecia najczesciej wystepujacych wartosci
top = df.describe().loc[["top"]].values[0]

# Sklejanie wartosci z listy top w jeden ciag znakow
gamma = ''
epsilon = ''
for _ in top:
    if _== '1':
        gamma += '1'
        epsilon += '0'
    else:
        gamma += '0'
        epsilon += '1'

#  int(string, 2) oznacza przekonwertowanie stringu zero-jedynek w systemie binarnym (2) na int
print("Power consumption of the submarine:",int(gamma, 2)*int(epsilon, 2))

# Rekurencyjne odfiltrowywanie kolejnych tablic na dwa sposoby
def rec(df, col: int, criteria: str):
    if criteria == "oxygen":
        if df.shape[0] > 1:
            while True:
                try:
                    filtered_df = df[df.iloc[:,col] == mode(df.iloc[:,col])]
                    col += 1
                    return rec(filtered_df, col, criteria)
                except:
                    filtered_df = df[df.iloc[:,col] == "1"]
                    col += 1
                    return rec(filtered_df, col, criteria)
        else:
            return df
    if criteria == "CO2":
        if df.shape[0] > 1:
            while True:
                try:
                    filtered_df = df[df.iloc[:,col] != mode(df.iloc[:,col])]
                    col += 1
                    return rec(filtered_df, col, criteria)
                except:
                    filtered_df = df[df.iloc[:,col] == "0"]
                    col += 1
                    return rec(filtered_df, col, criteria)
        else:
            return df
    else:
        print("Wrong criteria!")

# Funkcja sklejajaca elementy listy w jeden ciag znakow
def glue(arr: list):
    glued = ""
    for _ in arr:
        glued += _
    return glued

#  int(string, 2) oznacza przekonwertowanie stringu zero-jedynek w systemie binarnym (2) na int
oxygen = int(glue(rec(df, 0, "oxygen").values[0]), 2)
CO2 = int(glue(rec(df, 0, "CO2").values[0]), 2)

print("The life support rating:",oxygen*CO2)

# %% zadanie 4
day_four = get_data(session=S, day=4, year=2021)

drawn_numbers = [int(drawn) for drawn in day_four.split("\n\n")[0].split(",")]
boards = day_four.split("\n\n")[1:]

# Umieszczenie wszystkich elementow w jednej, dlugiej, tablicy i konwersja na tuplesy
long_tab = []
for board in boards:
    for row in board.split("\n"):
        for el in row.split():
            long_tab.append((int(el),0))

# znestowanie long_tab w liste list po 5 elementow
nested_tab = [long_tab[x:x+5] for x in range(0, len(long_tab), 5)]

# Sprawdzenie, czy wystepuje rzad lub wiersz jedynek dla zadanych indeksow
def check(dictionary: dict, key, index: int):
    col0 = []
    col1 = []
    # wyciagamy wagi dla wiersza przy wskazanym indeksie wiersza
    row = [_[1] for _ in dictionary[key]]
    # wyciagamy wagi i wartosci dla kolumny przy wskazanym indeksie kolumny
    for i in range(len(dictionary.keys())):
        col1.append(dictionary[i][index][1])
        col0.append(dictionary[i][index][0])
    if 0 not in col1:
        return 1, col0
    if 0 not in row:
        return 1, [_[0] for _ in dictionary[key]]
    else:
        return [0]

# Sprawdzenie tablicy/boardu po ilu krokach wystepuje bingo (jezeli wgl wystepuje)
def board_check(board: dict, drawns: list):
    copy_board = copy.deepcopy(board)
    # iterujemy po wylosowanych numerach
    for drawn in drawns:
        # sprawdzamy schodzac kolejno po wierszach
        for key in copy_board.keys():
            # sprawdzamy kolejne elementy w wierszu
            for (item, sign) in copy_board[key]:
                # jezeli niesprawdzony to znakujemy go 1-ka
                if item == drawn and sign == 0:
                    index = copy_board[key].index((item, sign))
                    copy_board[key][index] = (item, 1)
                    # sprawdzamy czy po tej zmianie, nie pojawila sie wygrana
                    temp = check(copy_board, key, index)
                    if temp[0] > 0:
                        return copy_board,temp[1],drawn,drawns.index(drawn)+1

# sprawdzenie kolejnych tablic
def find_board(numbers: list, long: list, nested: list, target: str):
    win = len(numbers)
    lost = 0
    for i in range(0,int(len(long)/5),5):
        temp_dict = dict(zip([_ for _ in range(0,5)],nested[i:i+5]))
        t = board_check(temp_dict, numbers)[3]
        if t <= win and target == "win":
            board,win_numb,last_drawn,t1 = board_check(temp_dict, numbers)
            win = t
        if t >= lost and target == "lost":
            board,win_numb,last_drawn,t1 = board_check(temp_dict, numbers)
            lost = t
    return board,win_numb,last_drawn,t1

# zsumowanie wyrazow niezaznaczonych
def game(numbers: list, long: list, nested: list, target: str):
    board,win_numb,last_drawn,t1 = find_board(numbers, long, nested, target)
    unmarked_sum = 0
    for rows in [_ for _ in board.values()]:
        for val in rows:
            if val[1] == 0:
                unmarked_sum += val[0]
                
    print("Final score is:",unmarked_sum*last_drawn)

game(drawn_numbers, long_tab, nested_tab, "win")
game(drawn_numbers, long_tab, nested_tab, "lost")

# %% zadanie 5
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
