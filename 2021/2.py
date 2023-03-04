from aocd import get_data
import yaml


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_two = get_data(session=S, day=2, year=2021)

# Slownik do zapisu polozenia
position = {"horizontal position": 0, "depth": 0}

# Obliczanie polozenia przez zmiany zapisow w slowniku
for M in day_two.split("\n"):
    temp = M.split(" ")
    if temp[0] == "forward":
        position["horizontal position"] += int(temp[1])
    if temp[0] == "down":
        position["depth"] += int(temp[1])
    if temp[0] == "up":
        position["depth"] -= int(temp[1])
print("horizontal*depth:", position["horizontal position"] * position["depth"])

# Slownik rozszerzony o aim
position = {"horizontal position": 0, "depth": 0, "aim": 0}

# Obliczanie polozenia przez zmiany zapisow w slowniku z uwzglednieniem aim
for M in day_two.split("\n"):
    temp = M.split(" ")
    if temp[0] == "forward":
        position["horizontal position"] += int(temp[1])
        position["depth"] += position["aim"] * int(temp[1])
    if temp[0] == "down":
        position["aim"] += int(temp[1])
    if temp[0] == "up":
        position["aim"] -= int(temp[1])
print(
    "horizontal*depth (with aim):", position["horizontal position"] * position["depth"]
)
