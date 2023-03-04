from aocd import get_data
import yaml
import copy


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_twelve = get_data(session=S, day=12, year=2021).split("\n")

# Szukanie sciezki w grafach w sposob losowy wraz z odrzucieniem juz pojawionych sie sciezek
# Przy czym, kazde przeszukiwanie wyrzuca odwiedzone "male jaskienie" (male litery)

tst1 = ["start-A", "start-b", "A-c", "A-b", "b-d", "A-end", "b-end"]

tst2 = [
    "dc-end",
    "HN-start",
    "start-kj",
    "dc-start",
    "dc-HN",
    "LN-dc",
    "HN-end",
    "kj-sa",
    "kj-HN",
    "kj-dc",
]

tst3 = [
    "fs-end",
    "he-DX",
    "fs-he",
    "start-DX",
    "pj-DX",
    "end-zg",
    "zg-sl",
    "zg-pj",
    "pj-he",
    "RW-he",
    "fs-DX",
    "pj-RW",
    "zg-RW",
    "start-pj",
    "he-WI",
    "zg-he",
    "pj-fs",
    "start-RW",
]


def add_vertex(graph, vertex):
    """Nowy wierzchołek do istniejącego grafu"""
    if vertex not in graph:
        graph[vertex] = []


def add_edge(graph, edge):
    """Dodaje nową krawędź (parę wierzchołków) do istniejącego grafu
    traktując graf nieskierowany prosty jako prosty graf skierowany, ale symetryczny i bez pętli
    """
    u, v = edge
    add_vertex(graph, u)
    add_vertex(graph, v)
    if u == v:
        raise ValueError("pętla!")
    if v not in graph[u]:
        graph[u].append(v)
    if u not in graph[v]:
        graph[v].append(u)


def make_graph(verts: list):
    graph = {}
    for row in verts:
        v = row.split("-")
        add_edge(graph, v)

    return graph


# def rand_path(graph):
#     g = copy.deepcopy(graph)
#     temp = ['start']

#     while (v != 'end'):
#         for v in g['start']:
#             temp.append(v)


#     return temp

# rand_path(tst)


def drop_it(graph, v):
    g = copy.deepcopy(graph)
    for el in g:
        try:
            g[el].remove(v)
        except:
            pass
    return g


tst = make_graph(tst1)
tst


def rand_path(graph, v):
    # print('v:',v)
    g = copy.deepcopy(graph)
    l = g[v]

    # print('temp before:',temp)
    # print('l before:',l)

    for _ in l:
        if _.islower() and _ in temp:
            # print('_.lower in temp:',_)
            l.remove(_)
    # if v.islower() and v in temp:
    #     print('v.lower in temp:',v)
    #     g = drop_it(g, v)
    # try:
    #     l.remove(v)
    # except:
    #     pass

    if "start" in l:
        l.remove("start")
    # print('l after:',l)
    randv = random.choice(l)
    # print('randv:',randv)
    if v == "start":
        if "start" not in temp:
            temp.append(v)
        g.pop(v)
    else:
        temp.append(v)

    if v == "end":
        return temp

    # print('temp after:',temp)

    # print('--------------------------')
    rand_path(g, randv)


ans = []
temp = []
rand_path(tst, "start")
temp
ans.append(temp)
ans


def iter_(graph: dict, i: int):
    ans = []
    for _ in range(i):
        try:
            temp = []
            temp = rand_path(graph, "start")
            ans.append(temp)
            print("temp:", temp)
        except:
            pass

    print("ans final", ans)
    final = []
    for el in ans:
        if el not in final:
            final.append(el)

    return final


iter_(tst, 100)

j = []
temp = []
rand_path(tst, "start")
j.append(temp)
j

drop_it(tst, "b")
