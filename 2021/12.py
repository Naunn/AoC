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


def DFS(
    graph: dict,
    vertex: str,
    destination: str,
    visited: list,
    path: list,
    VisitTwice: bool,
) -> int:
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
                visited[v] < 2 and (small_caves == 0 or v.isupper()) and VisitTwice
            ):
                count += DFS(graph, v, destination, visited, path, VisitTwice)

    path.pop()
    visited[vertex] = 0 if not VisitTwice else visited[vertex] - 1

    return count


def all_paths(graph: dict, start: str, finish: str, VisitTwice: bool) -> int:
    visited = dict.fromkeys(graph.keys(), 0)
    path = []
    visited[start] = 2
    return DFS(graph, start, finish, visited, path, VisitTwice)


all_paths(make_graph(tst1), "start", "end", False)  # 10
all_paths(make_graph(tst2), "start", "end", False)  # 19
all_paths(make_graph(tst3), "start", "end", False)  # 226

print(
    "There is {} paths through this cave system where we visit small caves at most once.".format(
        all_paths(make_graph(day_twelve), "start", "end", False)
    )
)

all_paths(make_graph(tst1), "start", "end", True)  # 36
all_paths(make_graph(tst2), "start", "end", True)  # 103
all_paths(make_graph(tst3), "start", "end", True)  # 3509

print(
    "There is {} paths through this cave system where we visit single small caves at most twice and other small caves at most once.".format(
        all_paths(make_graph(day_twelve), "start", "end", True)
    )
)
