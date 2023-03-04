from aocd import get_data
import yaml
import numpy as np


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_seven = get_data(session=S, day=7, year=2021)

positions = np.array([int(_) for _ in day_seven.split(",")])  # "a list comprehension"

tst = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def cheapest(pos: list):
    least = sum(pos)
    position = -1
    for pivot in pos:
        temp = 0
        for _ in pos:
            temp += ((pivot - _) ** 2) ** (1 / 2)
        if temp <= least:
            least = temp
            position = pivot
    return least, position


# cheapest(tst)

formation = cheapest(positions)
print(
    "The lowest possible fuel consumption is {} on position {}.".format(
        formation[0], formation[1]
    )
)


def series(number):
    temp = 0
    for _ in range(int(number) + 1):
        temp += _
    return temp


def cheapest_series(pos: list):
    least = sum(pos) * max(pos)
    position = -1

    for i in range(len(pos)):
        temp = 0

        for _ in pos:
            temp += series(((i - _) ** 2) ** (1 / 2))

        if temp <= least:
            least = temp
            position = i

    return least, position


# cheapest_series(tst)

formation = cheapest_series(positions)

print(
    "The lowest possible fuel consumption is {} on position {}.".format(
        formation[0], formation[1]
    )
)
