from aocd import get_data
import yaml
import copy
import numpy as np
import collections


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
puzzle_input = get_data(session=S, day=14, year=2021).split("\n")

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
# value_test(tst, tst_rules, 40, 2188189693529) # fails due to lack of memory

print(
    "The quantity of the most common element minus the quantity of the smallest element after 10 steps is {}.".format(
        polymer_value(puzzle_input[0], puzzle_input[2:], 10)
    )
)


def polymer_value(input_: str, rules_: str, i_: int):
    rules = rules_dict(rules_)

    # Initial counts of pairs
    init_counts = collections.Counter()
    for i in range(len(input_) - 1):
        init_counts[input_[i : i + 2]] += 1
        init_counts

    # Iterating and inputing another pairs
    for _ in range(i_):
        new_counts = collections.Counter()
        for k, v in init_counts.items():
            new_counts[
                f"{k[0]}{rules[k]}"
            ] += v  # take first letter in pair and concat with value from rules as new pair and add value
            new_counts[
                f"{rules[k]}{k[1]}"
            ] += v  # take value from rules and concat with second letter in pair as new pair and add value
        init_counts = new_counts

    # Counting each occurring letter and dividing by 2 (where the first and last leter from input_ get an extra +1)
    counts = collections.Counter()
    for k, v in init_counts.items():
        counts[f"{k[0]}"] += v
        counts[f"{k[1]}"] += v

    counts[input_[0]] += 1
    counts[input_[-1]] += 1

    val = np.array(list(counts.values())) // 2

    return max(val) - min(val)


value_test(tst, tst_rules, 10, 1588)
value_test(tst, tst_rules, 40, 2188189693529)

print(
    "The quantity of the most common element minus the quantity of the smallest element after 40 steps is {}.".format(
        polymer_value(puzzle_input[0], puzzle_input[2:], 40)
    )
)
