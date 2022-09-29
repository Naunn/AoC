# -*- coding: utf-8 -*-
"""
Created on Mon May 30 09:44:20 2022

@author: Bartosz Lewandowski
"""
# %% import
from aocd import get_data
#Prywatny
S = "53616c7465645f5fdf7a79d2869dc3fd8b6c0d014b4090d6eb88ddfcd11cb489d924af1b46d034ded8aac3e8fc992c6301dc38862fc0ddeb52e782efad13c7b1"
#Sluzbowy
# S = "53616c7465645f5fa3040137e8796b744f160c23166de45eded969b5f96733aa58d285abafac23502d030551882234ccaeeff4aaacf80fb20a6cae4036684707"
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

# %% zadanie 6
day_six = get_data(session=S, day=6, year=2021)

lanternfishes = np.array([int(_) for _ in day_six.split(',')]) # "a list comprehension"

tst = np.array([int(_) for _ in '3,4,3,1,2'.split(',')])

def born(fish: list):
    f = np.array(fish.copy())
    zeros = [i for i,x in enumerate(f) if x==0]
    if zeros != []:
        for _ in zeros:
            f[_] = 7
            f = np.append(f, 9)
        return f - 1
    else:
        return f - 1

def simulator(fishes: list, days: int):
    temp = born(fishes)
    for i in range(days-1):
        temp = born(temp)
    return len(temp)

# simulator(tst, 18) #26
# simulator(tst, 80) #5934
# simulator(tst, 256) #26984457539 - Too "long" to use the simulator()!

# print("The number of lanternfish after 80 days:",simulator(lanternfishes,80))

def evolution(tab: list):
    n = len(tab)-2
    # jezeli ustawimy ind = 0, to wyladujemy w tym samym miejscu
    # jezeli ind > 0, to modulo "przesunie" wskazywane wartosci o indeks "ind"
    # petla while uzupelnia liste o "przesuniete wartosci, a i jest zwyklym "wskaznikiem"
    ind = 1
    i = ind # dlatego i= ind, zeby nie zaczac wskazywac "zbyt wczesnie"
    # az do len(tab) + ind, bo zaczynamy ze wskaznikiem na pozycji ind,
    # a konczymy nie na dlugosci listy, lecz ind miejsc za nia
    temp1 = tab[0:n]
    temp2 = tab[n:9]
    temp = []
    while i < n + ind:
        temp.append(temp1[(i % n)])
        i += 1
    
    temp[6] += temp2[0]
    temp2[0] = temp2[1]
    temp2[1] = tab[0]
    
    return temp+temp2

# evolution([1, 1, 2, 1, 0, 0, 0, 0, 0])
# evolution([1, 2, 1, 0, 0, 0, 1, 0, 1])
# evolution([2, 1, 0, 0, 0, 1, 1, 1, 1])
# evolution([1, 0, 0, 0, 1, 1, 3, 1, 2])

def fish_number(start: list, days: int):
    # utworzenie inicjalnej tablicy
    fishes = [0]*9
    for _ in start:
        fishes[_] += 1
    
    day = 0
    while day < days:
        fishes = evolution(fishes)
        day += 1
        
    return fishes, sum(fishes)

# fish_number(tst, 18) #26
# fish_number(tst, 80) #5934
# fish_number(tst, 256) #26984457539

print("The number of lanternfish after 80 days:",fish_number(lanternfishes,80)[1])
print("The number of lanternfish after 80 days:",fish_number(lanternfishes,256)[1])

# %% zadanie 7
day_seven = get_data(session=S, day=7, year=2021)

positions = np.array([int(_) for _ in day_seven.split(',')]) # "a list comprehension"

tst = [16,1,2,0,4,2,7,1,2,14]

def cheapest(pos: list):
    least = sum(pos)
    position = -1
    for pivot in pos:
        temp = 0
        for _ in pos:
            temp += ((pivot-_)**2)**(1/2)
        if temp <= least:
            least = temp
            position = pivot
    return least, position

# cheapest(tst)

formation = cheapest(positions)
print("The lowest possible fuel consumption is {} on position {}.".format(formation[0],formation[1]))

def series(number):
    temp = 0
    for _ in range(int(number)+1):
        temp += _
    return temp

def cheapest_series(pos: list):
    least = sum(pos)*max(pos)
    position = -1
    
    for i in range(len(pos)):
        temp = 0
        
        for _ in pos:
            temp += series(((i-_)**2)**(1/2))
            
        if temp <= least:
            least = temp
            position = i
    
    return least, position

# cheapest_series(tst)

formation = cheapest_series(positions)

print("The lowest possible fuel consumption is {} on position {}.".format(formation[0],formation[1]))

# %% zadanie 8
day_eight = get_data(session=S, day=8, year=2021)

digit_legend = {'0': ['a','b','c','e','f','g'],
                '1': ['c','f'],
                '2': ['a','c','d','e','g'],
                '3': ['a','c','d','f','g'],
                '4': ['b','c','d','f'],
                '5': ['a','b','d','f','g'],
                '6': ['a','b','d','e','f','g'],
                '7': ['a','c','f'],
                '8': ['a','b','c','d','e','f','g'],
                '9': ['a','b','c','d','f','g']}

easy_digits = [_.split(' | ')[1].split(' ') for _ in day_eight.split('\n')]
decode_digits = [_.split(' | ')[0].split(' ') for _ in day_eight.split('\n')]

flat_easy_digits = [x for xs in easy_digits for x in xs]
# This is equivalent to:
# flat_list = []
# for xs in xss:
#     for x in xs:
#         flat_list.append(x)
sorted(decode_digits[0], key = len)
def easy_count(signal: list):
    one = 0
    four = 0
    seven = 0
    eight = 0
    for _ in signal:
        if len(_) == 2:
            one += 1
        if len(_) == 4:
            four += 1
        if len(_) == 3:
            seven += 1
        if len(_) == 7:
            eight += 1
            
    return one+four+seven+eight

print("The digits 1,4,7,8 appears {} times.".format(easy_count(flat_easy_digits)))

# tst_pos = [['acedgfb',
#         'cdfbe',
#         'gcdfa',
#         'fbcad',
#         'dab',
#         'cefabd',
#         'cdfgeb',
#         'eafb',
#         'cagedb',
#         'ab']]

def convert(list):
      
    # Converting integer list to string list
    s = [str(i) for i in list]
      
    # Join list items using join()
    res = int("".join(s))
      
    return(res)

def create_dict(positions: list, i: int):
    temp = sorted(positions[i], key = len) # Order words (ascending)
    # Create temporary dict of 100% correct numbers
    temp_dict = {1: set(temp[0]),
                 4: set(temp[2]),
                 7: set(temp[1]),
                 8: set(temp[9])}
    
    # Find 6,0,9 by comparing words of length 6 (we want to have len of difference equal to 1)
    if len(temp_dict[1]-set(temp[6])) == 1:     # checking for 6
        temp_dict[6] = set(temp[6])
    elif len(temp_dict[4]-set(temp[6])) == 1:   # checking for 0
        temp_dict[0] = set(temp[6])
    else:                                       # else 9
        temp_dict[9] = set(temp[6])
                
    if len(temp_dict[1]-set(temp[7])) == 1:     # checking for 6
        temp_dict[6] = set(temp[7])
    elif len(temp_dict[4]-set(temp[7])) == 1:   # checking for 0
        temp_dict[0] = set(temp[7])
    else:                                       # else 9
        temp_dict[9] = set(temp[7])
        
    if len(temp_dict[1]-set(temp[8])) == 1:     # checking for 6
        temp_dict[6] = set(temp[8])
    elif len(temp_dict[4]-set(temp[8])) == 1:   # checking for 0
        temp_dict[0] = set(temp[8])
    else:                                       # else 9
        temp_dict[9] = set(temp[8])        
    
    # Find 5,3,2 by comparing words of length 5 (we want to have len of difference equal to 1)
    if len(temp_dict[6]-set(temp[3])) == 1:     # checking for 5
        temp_dict[5] = set(temp[3])
    elif len(temp_dict[9]-set(temp[3])) == 1:   # checking for 3
        temp_dict[3] = set(temp[3])
    else:                                       # else 2
        temp_dict[2] = set(temp[3])
        
    if len(temp_dict[6]-set(temp[4])) == 1:     # checking for 5
        temp_dict[5] = set(temp[4])
    elif len(temp_dict[9]-set(temp[4])) == 1:   # checking for 3
        temp_dict[3] = set(temp[4])
    else:                                       # else 2
        temp_dict[2] = set(temp[4])

    if len(temp_dict[6]-set(temp[5])) == 1:     # checking for 5
        temp_dict[5] = set(temp[5])
    elif len(temp_dict[9]-set(temp[5])) == 1:   # checking for 3
        temp_dict[3] = set(temp[5])
    else:                                       # else 2
        temp_dict[2] = set(temp[5])

    return temp_dict

# tst_val = [['cdfeb', 'fcadb', 'cdfeb', 'cdbaf']]

def map_dict(coded: list, coded_values: list):
    final = 0
    
    for i in range(0,len(coded)):
        decoded_dict = create_dict(coded, i) # create decoded dictionary
        t = []
        
        # Searching through decoded dictionary
        for _ in coded_values[i]:
            for numb, key in decoded_dict.items():
                if key == set(_):
                    # Appending founded number to list
                    t.append(numb)
        # Converting list into whole number by cocnatenation and summing
        final += convert(t)
        
    return final

print("After adding all decoded values, we get: {}.".format(map_dict(decode_digits,easy_digits)))

# %% zadanie 9
day_nine = get_data(session=S, day=9, year=2021)

heightmap = np.array(([list(x) for x in day_nine.split('\n')]))

_map = []
for _input in heightmap:
    _map.append(list(map(int, _input)))

# def checker(input_map: list, i: int, j: int, rows: int, cols: int):   
    
#     check = int(input_map[i][j])
    
#     if i != rows and i != 0 and j != 0 and j != cols:
#         test = []
#         test.append(int(input_map[i-1][j]))
#         test.append(int(input_map[i+1][j]))
#         test.append(int(input_map[i][j-1]))
#         test.append(int(input_map[i][j+1]))

#         if check < min(test):
#             return check
#         else:
#             return -1
       
#     # CORNERS
#     # left up corner
#     if i == j == 0:
#         test = []
#         test.append(int(input_map[i][j+1]))
#         test.append(int(input_map[i+1][j]))
        
#         if check < min(test):
#             return check
#         else:
#             return -1
            
#     # right down corner
#     if i == j == rows == cols:
#         test = []
#         test.append(int(input_map[i][j-1]))
#         test.append(int(input_map[i-1][j]))
        
#         if check < min(test):
#             return check
#         else:
#             return -1
            
#     # right up corner
#     if i == 0 and j == cols:
#         test = []
#         test.append(int(input_map[i][j-1]))
#         test.append(int(input_map[i+1][j]))
        
#         if check < min(test):
#             return check
#         else:
#             return -1
 
#     # left down corner
#     if j == 0 and i == rows:
#         test = []
#         test.append(int(input_map[i][j+1]))
#         test.append(int(input_map[i-1][j]))
        
#         if check < min(test):
#             return check
#         else:
#             return -1
         
#     # EDGES
#     # up edge
#     if i == 0 and j != 0 and j != cols:
#         test = []
#         test.append(int(input_map[i+1][j]))
#         test.append(int(input_map[i][j-1]))
#         test.append(int(input_map[i][j+1]))

#         if check < min(test):
#             return check
#         else:
#             return -1
        
#     # down edge
#     if i == rows and j != 0 and j != cols:
#         test = []
#         test.append(int(input_map[i-1][j]))
#         test.append(int(input_map[i][j-1]))
#         test.append(int(input_map[i][j+1]))

#         if check < min(test):
#             return check
#         else:
#             return -1

#     # left edge
#     if j == 0 and i !=0 and i != rows:
#         test = []
#         test.append(int(input_map[i-1][j]))
#         test.append(int(input_map[i+1][j]))
#         test.append(int(input_map[i][j+1]))

#         if check < min(test):
#             return check
#         else:
#             return -1
      
#     # right edge
#     if j == cols and i !=0 and i != rows:
#         test = []
#         test.append(int(input_map[i-1][j]))
#         test.append(int(input_map[i+1][j]))
#         test.append(int(input_map[i][j-1]))

#         if check < min(test):
#             return check
#         else:
#             return -1
    
#     return -1

# def finder(input_map: list):
#     rows = np.shape(input_map)[0]-1
#     cols = np.shape(input_map)[1]-1
#     temp = []
    
#     # iterating through matrix, using checker() and adding values bigger then -1 to temp list
#     for i in range(0,rows+1):
#         for j in range(0,cols+1):
#             result = checker(input_map, i, j, rows, cols)
#             if result > -1:
#                 temp.append(result)
        
#     return temp
           
# tst = np.array([[2,1,9,9,9,4,3,2,1,0],
#                 [3,9,8,7,8,9,4,9,2,1],
#                 [9,8,5,6,7,8,9,8,9,2],
#                 [8,7,6,7,8,9,6,7,8,9],
#                 [9,8,9,9,9,6,5,6,7,8]])


# finder(tst)

# sum(np.array(finder(tst)))+len(np.array(finder(tst)))

# print("The sum of the risk levels of all low points on heightmap equals:",
#       sum(np.array(finder(heightmap)))+len(np.array(finder(heightmap))))

# Much shorter version
inputs = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678']
    
tst = []
for _input in inputs:
    tst.append(list(map(int, _input)))

def neighbuors(input_map: list, i, j):
    nghb = []
    
    # check to not cross bottom edge and append lower neighbour
    if i+1 < len(input_map):
        nghb.append(input_map[i+1][j])
    # check to not cross upper edge and append upper neighbour
    if i-1 >= 0:
        nghb.append(input_map[i-1][j])
    # check to not cross right edge and append right neighbour
    if j+1 < len(input_map[i]):
        nghb.append(input_map[i][j+1])
    # check to not cross left edge and append left neighbour
    if j-1 >= 0:
        nghb.append(input_map[i][j-1])
        
    return nghb
        
neighbuors(tst, 1, 1)

def lowest(input_map: list):
    result = 0
    
    # go through all points
    for i in range(len(input_map)):
        for j in range(len(input_map[i])):
            
            # check that the current point is the smallest of its neighbours
            if input_map[i][j] < min(neighbuors(input_map, i, j)):
                result += 1 + input_map[i][j]
                
    return result

lowest(tst)

print("The sum of the risk levels of all low points on heightmap equals:", lowest(_map))

# def lowest_points(input_map: list):
#     rows = np.shape(input_map)[0]-1
#     cols = np.shape(input_map)[1]-1
#     points_ij = []
    
#     for i in range(0,rows+1):
#         for j in range(0,cols+1):
#             result = checker(input_map, i, j, rows, cols)
#             if result > -1:
#                 points_ij.append([i,j])
#     return points_ij
           
# # points_list = lowest_points(heightmap)
# points_list = lowest_points(tst)
# # points_list[0]

# # Moze pseudo DFS (idziemy wglab i po natrafieniu na 9 cofamy)?
# def pseudoDFS(input_map: list, points: list, direction: None):
#     temp_input = input_map.copy()
#     i,j = points[0],points[1]
#     check = int(temp_input[i][j])

#     print(check, [i,j], "here")
#     temp_input[i][j] = -1
#     print(temp_input)
    
#     if i-1 >= 0 and 9 > int(temp_input[i-1][j]) >= 0:
#         print(input_map[i-1][j], [i-1,j], "up")
#         while (i-1 >= 0):
#             return pseudoDFS(temp_input, [i-1,j], "up")
#     elif i-2 >= 0 and 9 > int(temp_input[i-2][j]) >= 0 and 9 != int(temp_input[i-1][j]):
#         print(input_map[i-2][j], [i-2,j], "two up")
#         while (i-2 >= 0):
#             return pseudoDFS(temp_input, [i-2,j], "two up")
    
#     if j-1 >= 0 and 9 > int(temp_input[i][j-1]) >= 0:
#         print(input_map[i][j-1], [i,j-1], "left")
#         while (j-1 >= 0):
#             return pseudoDFS(temp_input, [i,j-1], "left")    
#     elif j-2 >= 0 and 9 > int(temp_input[i][j-2]) >= 0 and 9 != int(temp_input[i][j-1]):
#         print(input_map[i][j-2], [i,j-2], "two left")
#         while (j-2 >= 0):
#             return pseudoDFS(temp_input, [i,j-2], "two left")      
        
#     if j+1 <= np.shape(input_map)[1]-1 and 9 > int(temp_input[i][j+1]) >= 0:
#         print(input_map[i][j+1], [i,j+1], "right")
#         while (j+1 <= np.shape(input_map)[1]-1):
#             return pseudoDFS(temp_input, [i,j+1], "right") 
#     elif j+2 <= np.shape(input_map)[1]-1 and 9 > int(temp_input[i][j+2]) >= 0 and 9 != int(temp_input[i][j+1]):
#         print(input_map[i][j+2], [i,j+2], "two right")
#         while (j+2 <= np.shape(input_map)[1]-1):
#             return pseudoDFS(temp_input, [i,j+2], "two right")
    
#     if i+1 <= np.shape(input_map)[0]-1 and 9 > int(temp_input[i+1][j]) >= 0:
#         print(input_map[i+1][j], [i+1,j], "down")
#         while (i+1 <= np.shape(input_map)[0]-1):
#             return pseudoDFS(temp_input, [i+1,j], "down")
#     if i+2 <= np.shape(input_map)[0]-1 and 9 > int(temp_input[i+2][j]) >= 0 and 9 != int(temp_input[i+1][j]):
#         print(input_map[i+2][j], [i+2,j], "two down")
#         while (i+2 <= np.shape(input_map)[0]-1):
#             return pseudoDFS(temp_input, [i+2,j], "two down")
        
#     if direction == "up":
#         return pseudoDFS(temp_input, [i+1,j], "reverse")
#     if direction == "two up":
#         return pseudoDFS(temp_input, [i+2,j], "reverse")
    
#     if direction == "down":
#         return pseudoDFS(temp_input, [i-1,j], "reverse")
#     if direction == "two down":
#         return pseudoDFS(temp_input, [i-2,j], "reverse")
        
#     if direction == "left":
#         return pseudoDFS(temp_input, [i,j+1], "reverse")  
#     if direction == "two left":
#         return pseudoDFS(temp_input, [i,j+2], "reverse")  
    
#     if direction == "right":
#         return pseudoDFS(temp_input, [i,j-1], "reverse")
#     if direction == "two right":
#         return pseudoDFS(temp_input, [i,j-2], "reverse")
    
#     return temp_input

# print(tst)
# pseudoDFS(tst, points_list[2], None)
# pseudoDFS(tst, points_list[3], None)

# Much shorter version - We will be grouping by counting the number neighbours that are not 9 or
# over the edge for example [2,1,3,4] suggest that we have 4 groups with 2,1,3,4 members respectively
groups = []
def count_gr(temp: list, i, j):
    # break the loop if index is over the edge or on point equal 9 or already visited, i.e. equal to -1
    if i < 0 or i >= len(temp) or j <0 or j >= len(temp[i]) or temp[i][j] == 9 or temp[i][j] == -1:
        return
    
    # mark current point as visited
    temp[i][j] = -1
    # add mark (+1) to the last point from group
    groups[len(groups)-1] += 1
    # check same above condition for ALL neighbours to count if there is more of none nines
    count_gr(temp, i+1, j)
    count_gr(temp, i-1, j)
    count_gr(temp, i, j+1)
    count_gr(temp, i, j-1)

temp = copy.deepcopy(tst)
# go through all points in matrix
for i in range(len(temp)):
    for j in range(len(temp[i])):
        groups.append(0)
        count_gr(temp, i, j)

temp
# multiple three largest groups members like dot product
np.prod(sorted([x for x in groups if x != 0], reverse=True)[:3])

groups = []
temp = copy.deepcopy(_map)
for i in range(len(temp)):
    for j in range(len(temp[i])):
        groups.append(0)
        count_gr(temp, i, j)
        
print("The sum of the risk levels of all low points on heightmap equals:",
      np.prod(sorted([x for x in groups if x != 0], reverse=True)[:3]))

# %% zadanie 10
day_ten = get_data(session=S, day=10, year=2021)

syntax_ = day_ten.split('\n')

# {([(<{}[<>[]}>{[]{[(<()> drop {}, <>, [], [], ()
# {([(<[}>{{[(<> drop <>
# {([(<[}>{{[( found [}

# [[<[([]))<([[{}[[()]]] drop [], {}, ()
# [[<[())<([[[[]]] drop (), []
# [[<[)<([[[]] drop []
# [[<[)<([[] drop []
# [[<[)<([ found [)

# [{[{(]}([{[{{}([] drop {}, {}, {}
# [{[{(]}([{[{{}([] drop {}, []
# [{[{(]}([{[{( found (]

# [<(<(<(<{}))><([]([]() drop {}, [], [], ()
# [<(<(<(<))><(( found <)
                  
# <{([([[(<>()){}]>(<<{{ drop <>, (), {}
# <{([([[()]>(<<{{ drop ()
# <{([([[]>(<<{{ drop []
# <{([([>(<<{{ found [>

# Utowrzyc 3 tablice:
# pairs = ['()','[]','{}','<>']
# left_wing = ['(','[','{','<']
# right_wing =  [')',']','}','>']

# notatki:
# Przechodzac po kolejnych parach elementow sprawdzac czy znajduje sie w pairs i wyrzucic
# Powtarzac az do braku zmiany ilosci znakow w liscie
# Sprawdzic czy jak znajdziemy znak w left_wing, to czy jego sasiad z prawej jest w right_wing
# potrzeba bedzie jakos je ponumerowac
# zapewnienie, ze to nie bedzie para zapewnia nam wyrzucenie par w pierwszym kroku

tst = [
       '[({(<(())[]>[[{[]{<()<>>',
       '[(()[<>])]({[<{<<[]>>(',
       '{([(<{}[<>[]}>{[]{[(<()>',
       '(((({<>}<{<{<>}{[]{[]{}',
       '[[<[([]))<([[{}[[()]]]',
       '[{[{({}]{}}([{[{{{}}([]',
       '{<[[]]>}<{[{[{[]{()[[[]',
       '[<(<(<(<{}))><([]([]()',
       '<{([([[(<>()){}]>(<<{{',
       '<{([{{}}[<[[[<>{}]]]>[]]',
       ]

def corrupted(syntax: list):
    pairs = ['()','[]','{}','<>']
    right_wing =  [')',']','}','>']
    dict_ = {')': 3,
             ']': 57,
             '}': 1197,
             '>': 25137}
    crptd = []
    score = 0
    
    # Pick string from list of strings and convert it to list of chars using list()
    for k in range(len(syntax)):
        temp = list(syntax[k]) # temporary list (will be overwirited every iteration)
        j = [] # list of founded pairs
        
        # Iter through list of characters
        for iter in np.arange(len(temp)/2)+1: # length is enough to iterate multiple times
            
            # If list of pairs is none empty then pop pairs from list
            if len(j) > 0:
                for _ in sorted(j, reverse = True):
                    temp.pop(_)
                j = []
            else:
                # check if next two characters match any pair
                for i in range(len(temp)-1):
                    if temp[i]+temp[i+1] in pairs:
                        j.append(i)
                        j.append(i+1)
        
        # After removing all pairs, check if any right_wing sign occurs,
        # which indicate that there is an inappropriate match.
        for t in temp:
            if t in right_wing:
                crptd.append(t)
                break
    
    # count the score of founded mismatches by using dictionary values         
    for n in crptd:
        score += dict_[n]
    return score

corrupted(tst) # 26397 - good

print("The total syntax error score for those errors is:", corrupted(syntax_))

# Incomplete lines don't have any incorrect characters!
# [({(<(())[]>[[{[]{<()<>> drop (), [], [], (), <>
# [({(<()>[[{{<> drop (), <>
# [({(<>[[{{ drop <>
# [({([[{{ found }}]])})]

# [(()[<>])]({[<{<<[]>>( drop (), <>, []
# [([])]({[<{<<>>( drop [], <>
# [()]({[<{<>( drop (), <>
# []({[<{( drop []
# ({[<{( found )}>]})

# (((({<>}<{<{<>}{[]{[]{} drop <>, <>, [], [], {}
# (((({}<{<{}{{ drop {}, {}
# ((((<{<{{ found }}>}>))))

# {<[[]]>}<{[{[{[]{()[[[] drop [], [], (), []
# {<[]>}<{[{[{{[[ drop []
# {<>}<{[{[{{[[ drop <>
# {}<{[{[{{[[ drop {}
# <{[{[{{[[ found ]]}}]}]}>

# <{([{{}}[<[[[<>{}]]]>[]] drop {}, <>, {}, []
# <{([{}[<[[[]]]>] drop {}, []
# <{([[<[[]]>] drop []
# <{([[<[]>] drop []
# <{([[<>] drop <>
# <{([[] drop []
# <{([ found ])}>

# notatki:
# Dodac warunek do corrupted(), ktory nie sprawdza list "corrupted-owych"
# Usuwac pary analogicznie jak w corrupted()
# w incomplete nie sprawdzamy list gdzie wystepuja domkniecia nie do pary
# Utowrzyc dwa sloniki z pasujacymi wartosciami
# dopasowac lewe domkniecia do prawych po slownikach
# wykorzystac trzeci slownik zeby zliczyc wynik
    
def incomplete(syntax: list):
    pairs = ['()','[]','{}','<>']
    right_wing =  [')',']','}','>']
    right_wing_dict = {'(': ')',
                       '[': ']',
                       '{': '}',
                       '<': '>'}
    score_dict = {')': 1,
                  ']': 2,
                  '}': 3,
                  '>': 4}
    incmplt = []
    
    # Pick string from list of strings and convert it to list of chars using list()
    for k in range(len(syntax)):
        temp = list(syntax[k]) # temporary list (will be overwirited every iteration)
        j = [] # list of founded pairs
        
        # Iter through list of characters
        for iter in np.arange(len(temp)/2)+1: # length is enough to iterate multiple times
            
            # If list of pairs is none empty then pop pairs from list
            if len(j) > 0:
                for _ in sorted(j, reverse = True):
                    temp.pop(_)
                j = []
            else:
                # check if next two characters match any pair
                for i in range(len(temp)-1):
                    if temp[i]+temp[i+1] in pairs:
                        j.append(i)
                        j.append(i+1)
        
        # After removing all pairs, iterate through temp and count scores
        score = 0
        for t in temp[::-1]: # Remember to reverse order
            if t not in right_wing:
                score = score*5 + score_dict[right_wing_dict[t]]
            # In case of occuring corrupted pair, set score to 0 and break loop
            else:
                score = 0
                break
        
        incmplt.append(score)
        
    # Make sure to remove 0 values and return middle value
    final = sorted([_ for _ in incmplt if _ > 0])
    return final[int(len(final)/2)]

incomplete(tst)

print('The middle score is:', incomplete(syntax_))

# %% zadanie 11
day_eleven = get_data(session=S, day=11, year=2021).split('\n')

input_ = []
for inp in day_eleven:
    input_.append(list(map(int, inp)))

# notatki:
# rozwinac funkcje z zad 9 o sprawdzanie sasiadow po skosie
# w pierwszej kolejnosci w pierwszym kroku dodac wszytkim wartosciom +1
# dla kazdej osmiornicy, sprawdzic ile jej sasiadow jest rowna 10 i o taka liczba zwiekszyc jej wartosc
# powtarzac proces az do braku zmian (moze while macierz przed i po sa sobie rowne?)
# uwaga, jezeli osmiornica ma wartosc 10, to na razie jej nie ruszamy
# po braku zmian w macierzach, zamieniamy 10 na 0 (oznacza to zaswiecenie osmiornicy) i zliczamy ile takich bylo zmienionych
# jezeli byl w tym punkcie "blysk" to zamieniamy jego wartosc na 11-tke i juz wiecej nie ruszamy

tst_small = ['11111',
             '19991',
             '19191',
             '19991',
             '11111']

tst_big = ['5483143223',
           '2745854711',
           '5264556173',
           '6141336146',
           '6357385478',
           '4167524645',
           '2176841721',
           '6882881134',
           '4846848554',
           '5283751526']

tst = []
for _input in tst_big:
    tst.append(list(map(int, _input)))

# # iteration of:
# 6  5  9  4  2  5  4  3  3  4
# 3  8  5  6  9  6  5  8  2  2
# 6  3  7  5  6  6  7  2  8  4
# 7  2  5  2  4  4  7  2  5  7
# 7  4  6  8  4  9  6  5  8  9
# 5  2  7  8  6  3  5  7  5  6
# # all + 1:
# 7  6  10 5  3  6  5  4  4  5
# 4  9  6  7  10 7  6  9  3  3
# 7  4  8  6  7  7  8  3  9  5
# 8  3  6  3  5  5  8  3  6  8
# 8  5  7  9  5  10 7  6  9  10
# 6  3  8  9  7  4  6  8  6  7
# # first row 10's:
# 7  7  11 6  3  6  5  4  4  5
# 4  10 7  8  10 7  6  9  3  3
# 7  4  8  6  7  7  8  3  9  5
# 8  3  6  3  5  5  8  3  6  8
# 8  5  7  9  5  10 7  6  9  10
# 6  3  8  9  7  4  6  8  6  7
# # second row ten's:
# 8  8  11 7  4  7  5  4  4  5
# 5  11 8  9  11 8  6  9  3  3
# 8  5  9  7  8  8  8  3  9  5
# 8  3  6  3  5  5  8  3  6  8
# 8  5  7  9  5  10 7  6  9  10
# 6  3  8  9  7  4  6  8  6  7
# # fifth row ten's:
# 8  8  11 7  4  7  5  4  4  5
# 5  11 8  9  11 8  6  9  3  3
# 8  5  9  7  8  8  8  3  9  5
# 8  3  6  3  6  6  9  3  7  9
# 8  5  7  9  6  11 8  6  10 11
# 6  3  8  9  8  5  7  8  7  8
# # Repeat for finding 10's.
# # fifth row ten's
# 8  8  11 7  4  7  5  4  4  5
# 5  11 8  9  11 8  6  9  3  3
# 8  5  9  7  8  8  8  3  9  5
# 8  3  6  3  6  6  9  4  8  10
# 8  5  7  9  6  11 8  7  11 11
# 6  3  8  9  8  5  7  9  8  9
# # Repeat for finding 10's.
# # fourth row ten's
# 8  8  11 7  4  7  5  4  4  5
# 5  11 8  9  11 8  6  9  3  3
# 8  5  9  7  8  8  8  3  10 6
# 8  3  6  3  6  6  9  4  9  11
# 8  5  7  9  6  11 8  7  11 11
# 6  3  8  9  8  5  7  9  8  9
# # Repeat for finding 10's.
# # third row ten's
# 8  8  11 7  4  7  5  4  4  5
# 5  11 8  9  11 8  6  10 4  4
# 8  5  9  7  8  8  8  4  11 7
# 8  3  6  3  6  6  9  5  10 11
# 8  5  7  9  6  11 8  7  11 11
# 6  3  8  9  8  5  7  9  8  9
# # Repeat for finding 10's.
# # second row ten's
# 8  8  11 7  4  7  6  5  5  5
# 5  11 8  9  11 8  7  11 5  4
# 8  5  9  7  8  8  9  5  11 7
# 8  3  6  3  6  6  9  5  10 11
# 8  5  7  9  6  11 8  7  11 11
# 6  3  8  9  8  5  7  9  8  9
# # fourth row ten's
# 8  8  11 7  4  7  6  5  5  5
# 5  11 8  9  11 8  7  11 5  4
# 8  5  9  7  8  8  9  6  11 8
# 8  3  6  3  6  6  9  6  11 11
# 8  5  7  9  6  11 8  8  11 11
# 6  3  8  9  8  5  7  9  8  9
# # no further changes

# add 1 to all (if less then 10) noighbours
def oct_flash(input_map: list, i, j):
    input_map_ = copy.deepcopy(input_map)
    
    # vertical check
    # check to not cross bottom edge and append lower neighbour
    if i+1 < len(input_map) and input_map_[i+1][j] < 10:
        input_map_[i+1][j] += 1
    # check to not cross upper edge and append upper neighbour
    if i-1 >= 0 and input_map_[i-1][j] < 10:
        input_map_[i-1][j] += 1
        
    # horizontal check
    # check to not cross right edge and append right neighbour
    if j+1 < len(input_map[i]) and input_map_[i][j+1] < 10:
        input_map_[i][j+1] += 1
    # check to not cross left edge and append left neighbour
    if j-1 >= 0 and input_map_[i][j-1] < 10:
        input_map_[i][j-1] += 1
        
    # diagonal check
    # check to not cross upper left edge and append upper left neighbour
    if i-1 >= 0 and j-1 >= 0 and input_map_[i-1][j-1] < 10:
        input_map_[i-1][j-1] += 1
    # check to not cross upper right edge and append upper right neighbour
    if i-1 >= 0 and j+1 < len(input_map[i]) and input_map_[i-1][j+1] < 10:
        input_map_[i-1][j+1] += 1
    # check to not cross bottom left edge and append lower left neighbour
    if i+1 < len(input_map) and j-1 >= 0 and input_map_[i+1][j-1] < 10:
        input_map_[i+1][j-1] += 1
    # check to not cross bottom right edge and append lower right neighbour
    if i+1 < len(input_map) and j+1 < len(input_map[i]) and input_map_[i+1][j+1] < 10:
        input_map_[i+1][j+1] += 1
            
    return input_map_

oct_flash(tst, 2, 2) # add 1 to all nghbrs around

def flashes(input_map: list, iter_: int):
    result = 0
    input_map_ = np.array(copy.deepcopy(input_map))

    # iter
    for k in range(iter_):
        # as start add value to iteration
        input_map_ += 1

        # go through all points (repeat matrix dimension times, i.e. n x n - times - hard approach)
        for k in range(len(input_map)*len(input_map)):
            for i in range(len(input_map_)):
                for j in range(len(input_map_[i])):
                    # check if value is equal to 10 (10-th will be flashing octopuses)
                    if input_map_[i][j] == 10:
                        # add 1 to all noighbours < 10
                        input_map_ = oct_flash(input_map_,i,j)
                        # tag octopus as flashed i.e. = 11
                        input_map_[i][j] = 11
                    
        # count and overwrite 11 to 0
        result += np.count_nonzero(input_map_ == 11)
        input_map_[input_map_ == 11] = 0
        
    print("After", iter_,"step:\n")
    return input_map_, result

flashes(tst, 10) #204
flashes(tst, 100) #1656

print('After 100 steps there is a total number of flashes:', flashes(input_, 100)[1])

def bright(input_map: list, i: int):
    if (np.allclose([[0]*len(input_map)]*len(input_map), flashes(input_map, i)[0]) == False):
        return bright(input_map, i+1)
    else:
        return i

# bright(tst, 1) # after 195

# bright(input_, 1) # 324

print('The first step during which all octopuses flash is:', bright(input_, 324))

# %% zadanie 12
day_twelve = get_data(session=S, day=12, year=2021).split('\n')



























