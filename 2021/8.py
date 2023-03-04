from aocd import get_data
import yaml


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_eight = get_data(session=S, day=8, year=2021)

digit_legend = {
    "0": ["a", "b", "c", "e", "f", "g"],
    "1": ["c", "f"],
    "2": ["a", "c", "d", "e", "g"],
    "3": ["a", "c", "d", "f", "g"],
    "4": ["b", "c", "d", "f"],
    "5": ["a", "b", "d", "f", "g"],
    "6": ["a", "b", "d", "e", "f", "g"],
    "7": ["a", "c", "f"],
    "8": ["a", "b", "c", "d", "e", "f", "g"],
    "9": ["a", "b", "c", "d", "f", "g"],
}

easy_digits = [_.split(" | ")[1].split(" ") for _ in day_eight.split("\n")]
decode_digits = [_.split(" | ")[0].split(" ") for _ in day_eight.split("\n")]

flat_easy_digits = [x for xs in easy_digits for x in xs]
# This is equivalent to:
# flat_list = []
# for xs in xss:
#     for x in xs:
#         flat_list.append(x)
sorted(decode_digits[0], key=len)


def easy_count(signal: list):
    one = 0
    four = 0
    seven = 0
    eight = 0
    for _ in signal:
        if len(_) == 2:
            one += 1
        if len(_) == 4:
            four += 1
        if len(_) == 3:
            seven += 1
        if len(_) == 7:
            eight += 1

    return one + four + seven + eight


print("The digits 1,4,7,8 appears {} times.".format(easy_count(flat_easy_digits)))

# tst_pos = [['acedgfb',
#         'cdfbe',
#         'gcdfa',
#         'fbcad',
#         'dab',
#         'cefabd',
#         'cdfgeb',
#         'eafb',
#         'cagedb',
#         'ab']]


def convert(list):
    # Converting integer list to string list
    s = [str(i) for i in list]

    # Join list items using join()
    res = int("".join(s))

    return res


def create_dict(positions: list, i: int):
    temp = sorted(positions[i], key=len)  # Order words (ascending)
    # Create temporary dict of 100% correct numbers
    temp_dict = {1: set(temp[0]), 4: set(temp[2]), 7: set(temp[1]), 8: set(temp[9])}

    # Find 6,0,9 by comparing words of length 6 (we want to have len of difference equal to 1)
    if len(temp_dict[1] - set(temp[6])) == 1:  # checking for 6
        temp_dict[6] = set(temp[6])
    elif len(temp_dict[4] - set(temp[6])) == 1:  # checking for 0
        temp_dict[0] = set(temp[6])
    else:  # else 9
        temp_dict[9] = set(temp[6])

    if len(temp_dict[1] - set(temp[7])) == 1:  # checking for 6
        temp_dict[6] = set(temp[7])
    elif len(temp_dict[4] - set(temp[7])) == 1:  # checking for 0
        temp_dict[0] = set(temp[7])
    else:  # else 9
        temp_dict[9] = set(temp[7])

    if len(temp_dict[1] - set(temp[8])) == 1:  # checking for 6
        temp_dict[6] = set(temp[8])
    elif len(temp_dict[4] - set(temp[8])) == 1:  # checking for 0
        temp_dict[0] = set(temp[8])
    else:  # else 9
        temp_dict[9] = set(temp[8])

    # Find 5,3,2 by comparing words of length 5 (we want to have len of difference equal to 1)
    if len(temp_dict[6] - set(temp[3])) == 1:  # checking for 5
        temp_dict[5] = set(temp[3])
    elif len(temp_dict[9] - set(temp[3])) == 1:  # checking for 3
        temp_dict[3] = set(temp[3])
    else:  # else 2
        temp_dict[2] = set(temp[3])

    if len(temp_dict[6] - set(temp[4])) == 1:  # checking for 5
        temp_dict[5] = set(temp[4])
    elif len(temp_dict[9] - set(temp[4])) == 1:  # checking for 3
        temp_dict[3] = set(temp[4])
    else:  # else 2
        temp_dict[2] = set(temp[4])

    if len(temp_dict[6] - set(temp[5])) == 1:  # checking for 5
        temp_dict[5] = set(temp[5])
    elif len(temp_dict[9] - set(temp[5])) == 1:  # checking for 3
        temp_dict[3] = set(temp[5])
    else:  # else 2
        temp_dict[2] = set(temp[5])

    return temp_dict


# tst_val = [['cdfeb', 'fcadb', 'cdfeb', 'cdbaf']]


def map_dict(coded: list, coded_values: list):
    final = 0

    for i in range(0, len(coded)):
        decoded_dict = create_dict(coded, i)  # create decoded dictionary
        t = []

        # Searching through decoded dictionary
        for _ in coded_values[i]:
            for numb, key in decoded_dict.items():
                if key == set(_):
                    # Appending founded number to list
                    t.append(numb)
        # Converting list into whole number by cocnatenation and summing
        final += convert(t)

    return final


print(
    "After adding all decoded values, we get: {}.".format(
        map_dict(decode_digits, easy_digits)
    )
)
