from aocd import get_data
import yaml
from collections import Counter


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


def DFS(graph: dict, vertex: str, destination: str, visited: list, path: list) -> int:
    if vertex.islower():
        visited[vertex] = True
    path.append(vertex)

    count = 0
    if vertex == destination:
        count = 1
    else:
        for v in graph[vertex]:
            if visited[v] == False:
                count += DFS(graph, v, destination, visited, path)

    path.pop()
    visited[vertex] = False

    return count


def all_paths(graph: dict, start: str, finish: str) -> int:
    visited = dict.fromkeys(graph.keys(), False)
    path = []
    return DFS(graph, start, finish, visited, path)


all_paths(make_graph(tst1), "start", "end")  # 10
all_paths(make_graph(tst2), "start", "end")  # 19
all_paths(make_graph(tst3), "start", "end")  # 226

print(
    "There is {} paths through this cave system where we visit small caves at most once.".format(
        all_paths(make_graph(day_twelve), "start", "end")
    )
)


# def remove_bigger(x: list):
#     temp = x[1:-1]
#     for _ in temp:
#         if _.isupper():
#             temp.remove(_)
#     return temp


# def DFS_2(graph: dict, vertex: str, destination: str, visited: list, path: list) -> int:
#     if vertex.islower():
#         visited[vertex] += 1
#     path.append(vertex)

#     count = 0

#     #temp = remove_bigger(path)
#     if vertex == destination and (
#         len(temp) - 1 == len(set(temp)) or len(temp) == len(set(temp))
#     ):
#         count = 1
#     else:
#         for v in graph[vertex]:
#             if visited[v] < 2:  # and 2 not in list(visited.values())[1:]:
#                 count += DFS_2(graph, v, destination, visited, path)

#     path.pop()
#     visited[vertex] -= 1

#     return count


# def all_paths_2(graph: dict, start: str, finish: str) -> int:
#     visited = dict.fromkeys(graph.keys(), 0)
#     visited[start] = 2
#     visited[finish] = 1
#     path = []
#     return DFS_2(graph, start, finish, visited, path)


def DFS_2(graph: dict, vertex: str, destination: str, visited: list, path: list) -> int:
    if vertex.islower():
        visited[vertex] += 1
    path.append(vertex)

    count = 0

    if vertex == destination:
        count = 1
    else:
        small_caves = len(
            [
                item
                for item, count in Counter([i for i in path if i.islower()]).items()
                if count > 1
            ]
        )
        for v in graph[vertex]:
            if (visited[v] == 0) or (
                visited[v] < 2 and (small_caves == 0 or v.isupper())
            ):
                count += DFS_2(graph, v, destination, visited, path)

    path.pop()
    visited[vertex] -= 1

    return count


def all_paths_2(graph: dict, start: str, finish: str) -> int:
    visited = dict.fromkeys(graph.keys(), 0)
    path = []
    visited[start] = 2
    return DFS_2(graph, start, finish, visited, path)


all_paths_2(make_graph(tst1), "start", "end")  # 36
all_paths_2(make_graph(tst2), "start", "end")  # 103
all_paths_2(make_graph(tst3), "start", "end")  # 3509

print(
    "There is {} paths through this cave system where we visit single small caves at most twice and other small caves at most once.".format(
        all_paths_2(make_graph(day_twelve), "start", "end")
    )
)
