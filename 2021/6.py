from aocd import get_data
import yaml
import numpy as np


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_six = get_data(session=S, day=6, year=2021)

lanternfishes = np.array([int(_) for _ in day_six.split(",")])  # "a list comprehension"

tst = np.array([int(_) for _ in "3,4,3,1,2".split(",")])


def born(fish: list):
    f = np.array(fish.copy())
    zeros = [i for i, x in enumerate(f) if x == 0]
    if zeros != []:
        for _ in zeros:
            f[_] = 7
            f = np.append(f, 9)
        return f - 1
    else:
        return f - 1


def simulator(fishes: list, days: int):
    temp = born(fishes)
    for i in range(days - 1):
        temp = born(temp)
    return len(temp)


# simulator(tst, 18) #26
# simulator(tst, 80) #5934
# simulator(tst, 256) #26984457539 - Too "long" to use the simulator()!

# print("The number of lanternfish after 80 days:",simulator(lanternfishes,80))


def evolution(tab: list):
    n = len(tab) - 2
    # jezeli ustawimy ind = 0, to wyladujemy w tym samym miejscu
    # jezeli ind > 0, to modulo "przesunie" wskazywane wartosci o indeks "ind"
    # petla while uzupelnia liste o "przesuniete wartosci, a i jest zwyklym "wskaznikiem"
    ind = 1
    i = ind  # dlatego i= ind, zeby nie zaczac wskazywac "zbyt wczesnie"
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

    return temp + temp2


# evolution([1, 1, 2, 1, 0, 0, 0, 0, 0])
# evolution([1, 2, 1, 0, 0, 0, 1, 0, 1])
# evolution([2, 1, 0, 0, 0, 1, 1, 1, 1])
# evolution([1, 0, 0, 0, 1, 1, 3, 1, 2])


def fish_number(start: list, days: int):
    # utworzenie inicjalnej tablicy
    fishes = [0] * 9
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

print("The number of lanternfish after 80 days:", fish_number(lanternfishes, 80)[1])
print("The number of lanternfish after 80 days:", fish_number(lanternfishes, 256)[1])
