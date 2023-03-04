from aocd import get_data
import yaml
import pandas as pd
from statistics import mode


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_three = get_data(session=S, day=3, year=2021)

df = pd.DataFrame([list(M) for M in day_three.split("\n")])

# Wykorzystanie desc() do wyciagniecia najczesciej wystepujacych wartosci
top = df.describe().loc[["top"]].values[0]

# Sklejanie wartosci z listy top w jeden ciag znakow
gamma = ""
epsilon = ""
for _ in top:
    if _ == "1":
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"

#  int(string, 2) oznacza przekonwertowanie stringu zero-jedynek w systemie binarnym (2) na int
print("Power consumption of the submarine:", int(gamma, 2) * int(epsilon, 2))


# Rekurencyjne odfiltrowywanie kolejnych tablic na dwa sposoby
def rec(df, col: int, criteria: str):
    if criteria == "oxygen":
        if df.shape[0] > 1:
            while True:
                try:
                    filtered_df = df[df.iloc[:, col] == mode(df.iloc[:, col])]
                    col += 1
                    return rec(filtered_df, col, criteria)
                except:
                    filtered_df = df[df.iloc[:, col] == "1"]
                    col += 1
                    return rec(filtered_df, col, criteria)
        else:
            return df
    if criteria == "co2":
        if df.shape[0] > 1:
            while True:
                try:
                    filtered_df = df[df.iloc[:, col] != mode(df.iloc[:, col])]
                    col += 1
                    return rec(filtered_df, col, criteria)
                except:
                    filtered_df = df[df.iloc[:, col] == "0"]
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
co2 = int(glue(rec(df, 0, "co2").values[0]), 2)

print("The life support rating:", oxygen * co2)
