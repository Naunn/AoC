from aocd import get_data
import yaml
import numpy as np
import pandas as pd


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
puzzle_input = get_data(session=S, day=13, year=2021).split("\n")

folds = [fold for fold in puzzle_input if "x" in fold or "y" in fold]
dots = np.array(
    [[int(_) for _ in dot.split(",")] for dot in puzzle_input if "," in dot]
)

tst = [
    "6,10",
    "0,14",
    "9,10",
    "0,3",
    "10,4",
    "4,11",
    "6,0",
    "6,12",
    "4,1",
    "0,13",
    "10,12",
    "3,4",
    "3,0",
    "8,4",
    "1,10",
    "2,14",
    "8,10",
    "9,0",
    "fold along y=7",
    "fold along x=5",
]

folds_tst = [fold for fold in tst if "x" in fold or "y" in fold]
dots_tst = np.array([[int(_) for _ in dot.split(",")] for dot in tst if "," in dot])


def find_max(l_: np.array) -> tuple:
    x, y = 0, 0
    for el in l_:
        if el[0] >= x:
            x = el[0]
        if el[1] >= y:
            y = el[1]

    return x, y


def draw_dots(coords: np.array) -> np.array:
    width, length = find_max(coords)

    paper = np.array([["." for x in range(width + 1)] for y in range(length + 1)])

    for coord in coords:
        paper[coord[1]][coord[0]] = "#"

    return paper


def origami(coords: np.array, folds: np.array) -> np.array:
    set_ = set()
    for _ in coords:
        set_.add((_[0], _[1]))

    for fold in folds:
        axis, value = fold.split("=")[0][-1], int(fold.split("=")[-1])

        if axis == "x":
            set_ = {(x if x < value else value - (x - value), y) for x, y in set_}
        if axis == "y":
            set_ = {(x, y if y < value else value - (y - value)) for x, y in set_}

    coords_ = [[_[0], _[1]] for _ in set_]

    return draw_dots(coords_)


# origami(dots_tst, folds_tst)

print(
    "There are {} visible dots after first fold.".format(
        np.unique(origami(dots, [folds[0]]), return_counts=True)[1][0]
    )
)

pd.DataFrame(origami(dots, folds))
