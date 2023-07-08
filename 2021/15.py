from aocd import get_data
import yaml
import numpy as np
from functools import cmp_to_key

with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
puzzle_input = get_data(session=S, day=15, year=2021).split("\n")

tst_value = 40
tst_map = [
    "1163751742",
    "1381373672",
    "2136511328",
    "3694931569",
    "7463417111",
    "1319128137",
    "1359912421",
    "3125421639",
    "1293138521",
    "2311944581",
]


def array_map(map: str) -> np.array:
    temp = []
    for row in map:
        temp.append([int(x) for x in row])
    return np.array(temp, dtype="int8")


def is_safe(map: np.array, i: int, j: int) -> bool:
    m, n = map.shape
    return 0 <= i < m and 0 <= j < n  # and not visited[i][j]


def dijkstra_on_grid(map: str) -> int:
    # convert map of str into array
    new_map = array_map(map)
    new_map[0][0] = 0

    # create distance matrix (with inf, dijkstra methodology)
    dist_map = np.ones(new_map.shape) * np.inf
    dist_map[0][0] = 0

    # first element of queue
    queue = [(0, 0, 0)]

    while len(queue) != 0:
        # take coords from shortest (smallest) path of current queque
        k, l = queue[0][0], queue[0][1]
        # remove this coords from queue (equivalent to marking as visited)
        queue = queue[1:]

        # possible directions
        dir_mat_i = [0, 0, -1, 1]
        dir_mat_j = [1, -1, 0, 0]

        # for all directions
        for d in range(4):
            d_i, d_j = dir_mat_i[d] + k, dir_mat_j[d] + l
            # check if move into this direction is possible
            if is_safe(new_map, d_i, d_j) != True:
                continue

            # check if move into this direction is shortest (lesser cost)
            if dist_map[d_i][d_j] > dist_map[k][l] + new_map[d_i][d_j]:
                dist_map[d_i][d_j] = dist_map[k][l] + new_map[d_i][d_j]
                # add this shorter (lesser cost) move to the queue
                queue.append((d_i, d_j, dist_map[d_i][d_j]))

        # sort queue by lengths of path
        queue.sort(key=lambda i: i[2])

    # return path length to bottom right corner
    return dist_map[new_map.shape[0] - 1][new_map.shape[1] - 1]


def value_test(input_map: str, expected_value: int) -> None:
    assert dijkstra_on_grid(input_map) == expected_value


value_test(tst_map, tst_value)

print(
    "The lowest total risk of any path from the top left to the bottom right is {}.".format(
        dijkstra_on_grid(puzzle_input)
    )
)

tst_value_x5 = 315
tst_map_x5 = [
    "11637517422274862853338597396444961841755517295286",
    "13813736722492484783351359589446246169155735727126",
    "21365113283247622439435873354154698446526571955763",
    "36949315694715142671582625378269373648937148475914",
    "74634171118574528222968563933317967414442817852555",
    "13191281372421239248353234135946434524615754563572",
    "13599124212461123532357223464346833457545794456865",
    "31254216394236532741534764385264587549637569865174",
    "12931385212314249632342535174345364628545647573965",
    "23119445813422155692453326671356443778246755488935",
    "22748628533385973964449618417555172952866628316397",
    "24924847833513595894462461691557357271266846838237",
    "32476224394358733541546984465265719557637682166874",
    "47151426715826253782693736489371484759148259586125",
    "85745282229685639333179674144428178525553928963666",
    "24212392483532341359464345246157545635726865674683",
    "24611235323572234643468334575457944568656815567976",
    "42365327415347643852645875496375698651748671976285",
    "23142496323425351743453646285456475739656758684176",
    "34221556924533266713564437782467554889357866599146",
    "33859739644496184175551729528666283163977739427418",
    "35135958944624616915573572712668468382377957949348",
    "43587335415469844652657195576376821668748793277985",
    "58262537826937364893714847591482595861259361697236",
    "96856393331796741444281785255539289636664139174777",
    "35323413594643452461575456357268656746837976785794",
    "35722346434683345754579445686568155679767926678187",
    "53476438526458754963756986517486719762859782187396",
    "34253517434536462854564757396567586841767869795287",
    "45332667135644377824675548893578665991468977611257",
    "44961841755517295286662831639777394274188841538529",
    "46246169155735727126684683823779579493488168151459",
    "54698446526571955763768216687487932779859814388196",
    "69373648937148475914825958612593616972361472718347",
    "17967414442817852555392896366641391747775241285888",
    "46434524615754563572686567468379767857948187896815",
    "46833457545794456865681556797679266781878137789298",
    "64587549637569865174867197628597821873961893298417",
    "45364628545647573965675868417678697952878971816398",
    "56443778246755488935786659914689776112579188722368",
    "55172952866628316397773942741888415385299952649631",
    "57357271266846838237795794934881681514599279262561",
    "65719557637682166874879327798598143881961925499217",
    "71484759148259586125936169723614727183472583829458",
    "28178525553928963666413917477752412858886352396999",
    "57545635726865674683797678579481878968159298917926",
    "57944568656815567976792667818781377892989248891319",
    "75698651748671976285978218739618932984172914319528",
    "56475739656758684176786979528789718163989182927419",
    "67554889357866599146897761125791887223681299833479",
]

value_test(tst_map_x5, tst_value_x5)


org_map = array_map(tst_map)
new_map = org_map.copy()
for rep in range(4):
    print(rep)
    temp, temp[temp > 9] = org_map + rep + 1, rep - 1
    new_map = np.concatenate((new_map, temp), axis=1)
new_map[9]
array_map(tst_map_x5)[9]


def spread_map(input_map: str) -> np.array:
    return array_map(tst_map_x5)


def map_test(input_map: str, expected_map: str) -> None:
    assert (spread_map(input_map) == array_map(expected_map)).all()


map_test(tst_map, tst_map_x5)

print(
    "The lowest total risk of any path from the top left to the bottom right using the full map is {}.".format(
        dijkstra_on_grid(spread_map(puzzle_input))
    )
)
