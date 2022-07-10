# -*- coding: utf-8 -*-
"""
Created on Mon May 30 09:44:20 2022

@author: Bartosz Lewandowski
"""
# %% import
from aocd import get_data
#Prywatny
# S = "53616c7465645f5f14044fb9e9c8529fb52cd27efaee89e40ccc4a65b109fd6eef45152740499f22ab9faf1e9d33d299f44dabccb491f0da6643251321077c66"
#Sluzbowy
S = "53616c7465645f5fa3040137e8796b744f160c23166de45eded969b5f96733aa58d285abafac23502d030551882234ccaeeff4aaacf80fb20a6cae4036684707"
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


def checker(input_map: list, i: int, j: int, rows: int, cols: int):   
    
    check = int(input_map[i][j])
    
    if i != rows and i != 0 and j != 0 and j != cols:
        test = []
        test.append(int(input_map[i-1][j]))
        test.append(int(input_map[i+1][j]))
        test.append(int(input_map[i][j-1]))
        test.append(int(input_map[i][j+1]))

        if check < min(test):
            return check
       
    # CORNERS
    # left up corner
    if i == j == 0:
        test = []
        test.append(int(input_map[i][j+1]))
        test.append(int(input_map[i+1][j]))
        print("left up corner")
        if check < min(test):
            return check
            
    # right down corner
    if i == j == rows == cols:
        test = []
        test.append(int(input_map[i][j-1]))
        test.append(int(input_map[i-1][j]))
        
        if check < min(test):
            return check
            
    # right up corner
    if i == 0 and j == cols:
        test = []
        test.append(int(input_map[i][j-1]))
        test.append(int(input_map[i+1][j]))
        print("right up corner")
        if check < min(test):
            return check
 
    # left down corner
    if i == 0 and j == cols:
        test = []
        test.append(int(input_map[i][j+1]))
        test.append(int(input_map[i-1][j]))
        
        if check < min(test):
            return check
         
    # EDGES
    # up edge
    if i == 0:
        test = []
        test.append(int(input_map[i+1][j]))
        test.append(int(input_map[i][j-1]))
        test.append(int(input_map[i][j+1]))

        if check < min(test):
            return check
        
    # down edge
    if i == rows:
        test = []
        test.append(int(input_map[i-1][j]))
        test.append(int(input_map[i][j-1]))
        test.append(int(input_map[i][j+1]))

        if check < min(test):
            return check

    # left edge
    if j == 0:
        test = []
        test.append(int(input_map[i-1][j]))
        test.append(int(input_map[i+1][j]))
        test.append(int(input_map[i][j+1]))

        if check < min(test):
            return check
      
    # right edge
    if j == cols:
        test = []
        test.append(int(input_map[i-1][j]))
        test.append(int(input_map[i+1][j]))
        test.append(int(input_map[i][j-1]))

        if check < min(test):
            return check

    return -1

def searcher(input_map: list):
    rows = np.shape(input_map)[0]
    cols = np.shape(input_map)[1]
    temp = []
    
    for i in range(0,rows):
        for j in range(0,cols):
            result = checker(input_map, i, j, rows, cols)
            if result > -1:
                temp.append(result)
        
    return temp
           
sum(np.array(searcher(heightmap)))

len(np.array(searcher(heightmap)))

tst = np.array([[2,1,9,9,9,4,3,2,1,0],
                [3,9,8,7,8,9,4,9,2,1],
                [9,8,5,6,7,8,9,8,9,2],
                [8,7,6,7,8,9,6,7,8,9],
                [9,8,9,9,9,6,5,6,7,8]])

tst[0][1]

searcher(tst)

tst[1][0]

checker(heightmap, 34, 97, 100, 100)
heightmap[34][97]

[x for x in range(0,10)]



























