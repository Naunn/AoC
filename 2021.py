# -*- coding: utf-8 -*-
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
# %% zadanie 1
day_one = get_data(session=S, day=1, year=2021)

# Przeniesienie przekonwertowanych pomiarów do listy.
# Nie mozna wrzucic w set, bo "zjada" wartosci. Z 2000 do 1639.
measurement = []
for M in day_one.split('\n'):
    measurement.append(int(M))
    
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

position = {"horizontal position": 0,
            "depth": 0}

for M in day_two.split('\n'):
    temp = M.split(" ")
    if temp[0] == "forward":
        position["horizontal position"] += int(temp[1])
    if temp[0] == "down":
        position["depth"] += int(temp[1])
    if temp[0] == "up":
        position["depth"] -= int(temp[1])
print(position["horizontal position"]*position["depth"])

position = {"horizontal position": 0,
            "depth": 0,
            "aim": 0}

for M in day_two.split('\n'):
    temp = M.split(" ")
    if temp[0] == "forward":
        position["horizontal position"] += int(temp[1])
        position["depth"] += position["aim"]*int(temp[1])
    if temp[0] == "down":
        position["aim"] += int(temp[1])
    if temp[0] == "up":
        position["aim"] -= int(temp[1])
print(position["horizontal position"]*position["depth"])

# %% zadanie 3
day_three = get_data(session=S, day=3, year=2021)

df = pd.DataFrame([list(M) for M in day_three.split("\n")])

top = df.describe().loc[["top"]].values[0]

gamma = ''
epsilon = ''
for _ in top:
    if _== '1':
        gamma += '1'
        epsilon += '0'
    else:
        gamma += '0'
        epsilon += '1'

print("Power consumption of the submarine:",int(gamma, 2)*int(epsilon, 2))

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

def glue(arr: list):
    glued = ""
    for _ in arr:
        glued += _
    return glued

oxygen = int(glue(rec(df, 0, "oxygen").values[0]), 2)
CO2 = int(glue(rec(df, 0, "CO2").values[0]), 2)

print("The life support rating:",oxygen*CO2)






