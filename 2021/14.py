from aocd import get_data
import yaml
import copy
import numpy as np


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
puzzle_input = get_data(session=S, day=14, year=2021).split("\n")
puzzle_input[2:]

tst = "NNCB"
tst_rules = [
    "CH -> B",
    "HH -> N",
    "CB -> H",
    "NH -> C",
    "HB -> C",
    "HC -> B",
    "HN -> C",
    "NN -> C",
    "BH -> H",
    "NC -> B",
    "NB -> B",
    "BN -> B",
    "BB -> N",
    "BC -> B",
    "CC -> N",
    "CN -> C",
]


def rules_dict(list_: list) -> dict:
    dict_ = {}
    for _ in list_:
        key, value = _.split(" -> ")
        dict_[key] = value

    return dict_


def polymer_template(template: str, rules: list, n: int) -> str:
    i = 0
    temp = list(copy.copy(template))

    while i < n:
        for j in range(len(temp) - 1):
            temp = (
                temp[: j * 2 + 1]
                + [rules_dict(rules)[template[j] + template[j + 1]]]
                + temp[j * 2 + 1 :]
            )
        template = temp

        i += 1

    return "".join(template)


def str_test(input_s: str, input_d: dict, input_i: int, expected: str) -> None:
    assert polymer_template(input_s, input_d, input_i) == expected


str_test(tst, tst_rules, 1, "NCNBCHB")
str_test(tst, tst_rules, 2, "NBCCNBBBCBHCB")
str_test(tst, tst_rules, 3, "NBBBCNCCNBBNBNBBCHBHHBCHB")
str_test(tst, tst_rules, 4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")


def polymer_value(template: str, rules: list, n: int) -> int:
    polymer_string = list(polymer_template(template, rules, n))

    counts = np.unique(polymer_string, return_counts=True)[1]

    return max(counts) - min(counts)


def value_test(input_s: str, input_d: dict, input_i: int, expected: int) -> None:
    assert polymer_value(input_s, input_d, input_i) == expected


value_test(tst, tst_rules, 10, 1588)
value_test(tst, tst_rules, 40, 2188189693529)

print(
    "The quantity of the most common element minus the quantity of the smallest element after 10 steps is {}.".format(
        polymer_value(puzzle_input[0], puzzle_input[2:], 10)
    )
)

print(
    "The quantity of the most common element minus the quantity of the smallest element after 40 steps is {}.".format(
        polymer_value(puzzle_input[0], puzzle_input[2:], 40)
    )
)
