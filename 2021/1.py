from aocd import get_data
import yaml


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_one = get_data(session=S, day=1, year=2021)

# Przeniesienie przekonwertowanych pomiarów do listy.
# Nie mozna wrzucic w set, bo "zjada" wartosci. Z 2000 do 1639.
measurement = []
for M in day_one.split("\n"):
    measurement.append(int(M))


# Zliczanie increase i decrease
def incr_decr(measures: list):
    increase = 0
    decrease = 0
    for i in range(1, len(measures)):
        if measures[i] > measures[i - 1]:
            increase += 1
        if measures[i] < measures[i - 1]:
            decrease += 1

    print("increase = {} \ndecrease = {}".format(increase, decrease))


incr_decr(measurement)

# Zsumowanie 3 kolejnych pomiarow i zapisanie w jednej liscie
measurement_3 = []
for i in range(len(measurement) - 2):
    measurement_3.append(measurement[i] + measurement[i + 1] + measurement[i + 2])

incr_decr(measurement_3)
