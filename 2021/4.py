from aocd import get_data
import yaml
import copy


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_four = get_data(session=S, day=4, year=2021)

drawn_numbers = [int(drawn) for drawn in day_four.split("\n\n")[0].split(",")]
boards = day_four.split("\n\n")[1:]

# Umieszczenie wszystkich elementow w jednej, dlugiej, tablicy i konwersja na tuplesy
long_tab = []
for board in boards:
    for row in board.split("\n"):
        for el in row.split():
            long_tab.append((int(el), 0))

# znestowanie long_tab w liste list po 5 elementow
nested_tab = [long_tab[x : x + 5] for x in range(0, len(long_tab), 5)]


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
            for item, sign in copy_board[key]:
                # jezeli niesprawdzony to znakujemy go 1-ka
                if item == drawn and sign == 0:
                    index = copy_board[key].index((item, sign))
                    copy_board[key][index] = (item, 1)
                    # sprawdzamy czy po tej zmianie, nie pojawila sie wygrana
                    temp = check(copy_board, key, index)
                    if temp[0] > 0:
                        return copy_board, temp[1], drawn, drawns.index(drawn) + 1


# sprawdzenie kolejnych tablic
def find_board(numbers: list, long: list, nested: list, target: str):
    win = len(numbers)
    lost = 0
    for i in range(0, int(len(long) / 5), 5):
        temp_dict = dict(zip([_ for _ in range(0, 5)], nested[i : i + 5]))
        t = board_check(temp_dict, numbers)[3]
        if t <= win and target == "win":
            board, win_numb, last_drawn, t1 = board_check(temp_dict, numbers)
            win = t
        if t >= lost and target == "lost":
            board, win_numb, last_drawn, t1 = board_check(temp_dict, numbers)
            lost = t
    return board, win_numb, last_drawn, t1


# zsumowanie wyrazow niezaznaczonych
def game(numbers: list, long: list, nested: list, target: str):
    board, win_numb, last_drawn, t1 = find_board(numbers, long, nested, target)
    unmarked_sum = 0
    for rows in [_ for _ in board.values()]:
        for val in rows:
            if val[1] == 0:
                unmarked_sum += val[0]

    print("Final score is:", unmarked_sum * last_drawn)


game(drawn_numbers, long_tab, nested_tab, "win")
game(drawn_numbers, long_tab, nested_tab, "lost")
