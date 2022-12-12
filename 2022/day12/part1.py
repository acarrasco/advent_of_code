import sys
import pprint
import numpy
from itertools import zip_longest
from collections import defaultdict

ADJACENCY = [
    (1, 0), (-1, 0), (0, -1), (0, 1),
]

inf = float('inf')

def a_star(start, goal, neighbors, d, h):
    open_set = {start}

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)

    while open_set:
        current = min(open_set, key=f_score.__getitem__)
        if current == goal:
            print(g_score)
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


def parse(lines):
    acode = ord('a')
    heightmap = []
    for i, row in enumerate(lines):
        r = []
        for j, c in enumerate(row.strip()):
            if c == 'S':
                start = i, j
                h = 0
            elif c == 'E':
                end = i, j
                h = ord('z') - acode
            else:
                h = ord(c) - acode
            r.append(h)
        heightmap.append(r)
    return heightmap, start, end

def solve(heightmap, start, end):
    rows = len(heightmap)
    cols = len(heightmap[0])

    print(numpy.array(heightmap))

    def neighbors(a):
        ai, aj = a
        for di, dj in ADJACENCY:
            ni, nj = ai + di, aj + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                ah = heightmap[ai][aj]
                nh = heightmap[ni][nj]
                if ah + 1 >= nh:
                    yield ni, nj
    def h(a):
        ai, aj = a
        ei, ej = end
        return abs(ai - ei) + abs(ai - ei)

    def d(current, neighbor):
        return 1

    solution = a_star(start, end, neighbors, d, h)
    return solution

lines = sys.stdin.readlines()
print(solve(*parse(lines)))