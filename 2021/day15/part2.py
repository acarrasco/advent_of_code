import sys
import re
from collections import defaultdict

adjacency = [(i, j) for i in (-1, 0, 1)
             for j in (-1, 0, 1) if bool(i) ^ bool(j)]

inf = float('inf')


def get_neighbors(rows, columns, i, j):
    for di, dj in adjacency:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < columns:
            yield ni, nj


def parse_line(line):
    return tuple(map(int, line.strip()))


def parse(lines):
    return tuple(filter(None, map(parse_line, lines)))


def a_star(start, goal, neighbors, d, h):
    open_set = {start}

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)

    while open_set:
        current = min(open_set, key=f_score.__getitem__)
        if current == goal:
            return g_score[current]

        open_set.remove(current)
        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + d(current, neighbor)
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                fs = tentative_g_score + h(neighbor)
                if fs != inf:
                    f_score[neighbor] = fs
                open_set.add(neighbor)
    return None


def top_down_reductions(reduction_rules, molecule):
    for src, dst in reduction_rules.items():
        for m in re.finditer(src, molecule):
            yield molecule[:m.start()] + dst + molecule[m.end():]


def expand_caves(caves, times=5):
    r, c = len(caves), len(caves[0])
    res = [[0] * c*times for _ in range(times*r)]
    for i in range(r):
        for j in range(c):
            for ti in range(times):
                for tj in range(times):
                    v = caves[i][j]

                    res[i+r*ti][j+c*tj] = 1 + (v-1+ti+tj) % 9
    return res


caves = expand_caves(parse(sys.stdin.readlines()))


rows = len(caves)
columns = len(caves[0])


def distance(_a, b):
    i, j = b
    return caves[i][j]


def heuristic(p):
    i, j = p
    return abs(rows - i) + abs(rows - j)


def neighbors(p):
    i, j = p
    return tuple(get_neighbors(rows, columns, i, j))


print(a_star((0, 0), (rows-1, columns-1), neighbors, distance, heuristic))
