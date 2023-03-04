from aocd import get_data
import yaml
import numpy as np
import copy


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_eleven = get_data(session=S, day=11, year=2021).split("\n")

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

tst_small = ["11111", "19991", "19191", "19991", "11111"]

tst_big = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]

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
    if i + 1 < len(input_map) and input_map_[i + 1][j] < 10:
        input_map_[i + 1][j] += 1
    # check to not cross upper edge and append upper neighbour
    if i - 1 >= 0 and input_map_[i - 1][j] < 10:
        input_map_[i - 1][j] += 1

    # horizontal check
    # check to not cross right edge and append right neighbour
    if j + 1 < len(input_map[i]) and input_map_[i][j + 1] < 10:
        input_map_[i][j + 1] += 1
    # check to not cross left edge and append left neighbour
    if j - 1 >= 0 and input_map_[i][j - 1] < 10:
        input_map_[i][j - 1] += 1

    # diagonal check
    # check to not cross upper left edge and append upper left neighbour
    if i - 1 >= 0 and j - 1 >= 0 and input_map_[i - 1][j - 1] < 10:
        input_map_[i - 1][j - 1] += 1
    # check to not cross upper right edge and append upper right neighbour
    if i - 1 >= 0 and j + 1 < len(input_map[i]) and input_map_[i - 1][j + 1] < 10:
        input_map_[i - 1][j + 1] += 1
    # check to not cross bottom left edge and append lower left neighbour
    if i + 1 < len(input_map) and j - 1 >= 0 and input_map_[i + 1][j - 1] < 10:
        input_map_[i + 1][j - 1] += 1
    # check to not cross bottom right edge and append lower right neighbour
    if (
        i + 1 < len(input_map)
        and j + 1 < len(input_map[i])
        and input_map_[i + 1][j + 1] < 10
    ):
        input_map_[i + 1][j + 1] += 1

    return input_map_


oct_flash(tst, 2, 2)  # add 1 to all nghbrs around


def flashes(input_map: list, iter_: int):
    result = 0
    input_map_ = np.array(copy.deepcopy(input_map))

    # iter
    for k in range(iter_):
        # as start add value to iteration
        input_map_ += 1

        # go through all points (repeat matrix dimension times, i.e. n x n - times - hard approach)
        for k in range(len(input_map) * len(input_map)):
            for i in range(len(input_map_)):
                for j in range(len(input_map_[i])):
                    # check if value is equal to 10 (10-th will be flashing octopuses)
                    if input_map_[i][j] == 10:
                        # add 1 to all noighbours < 10
                        input_map_ = oct_flash(input_map_, i, j)
                        # tag octopus as flashed i.e. = 11
                        input_map_[i][j] = 11

        # count and overwrite 11 to 0
        result += np.count_nonzero(input_map_ == 11)
        input_map_[input_map_ == 11] = 0

    print("After", iter_, "step:\n")
    return input_map_, result


flashes(tst, 10)  # 204
flashes(tst, 100)  # 1656

print("After 100 steps there is a total number of flashes:", flashes(input_, 100)[1])


def bright(input_map: list, i: int):
    if (
        np.allclose([[0] * len(input_map)] * len(input_map), flashes(input_map, i)[0])
        == False
    ):
        return bright(input_map, i + 1)
    else:
        return i


# bright(tst, 1) # after 195

# bright(input_, 1) # 324

print("The first step during which all octopuses flash is:", bright(input_, 324))
