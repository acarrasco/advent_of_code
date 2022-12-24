import sys
from collections import defaultdict
from math import inf, gcd

DIRECTIONS_MAP = {
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '^': (-1, 0),
}

DIRECTIONS_REVERSE_MAP = {d: c for c, d in DIRECTIONS_MAP.items()}

DIRECTIONS = list(DIRECTIONS_MAP.values()) + [(0, 0)]

def print_blizzards(blizzards, rows, cols):
    m = [['.' for _ in range(cols)] for _ in range(rows)]
    for (i,j), d in blizzards:
        if m[i][j] == '.':
            m[i][j] = DIRECTIONS_REVERSE_MAP[d]
        elif m[i][j] in DIRECTIONS_MAP:
            m[i][j] = '2'
        else:
            m[i][j] = str(int(m[i][j]) + 1)
    print('#.' + '#'*cols)
    for row in m:
        print('#' + ''.join(row) + '#')
    print('#' * cols + '.#')
    print()

def parse(lines):
    blizzards = []

    for i, row in enumerate(lines):
        for j, c in enumerate(row.strip()):
            d = DIRECTIONS_MAP.get(c)
            if d:
                p = i - 1, j - 1
                blizzards.append((p, d)) # discount walls
    rows = i - 1
    cols = j - 1
    return blizzards, rows, cols

def update_blizzards(blizzards, rows, cols):
    return [
        (((i + di) % rows, (j + dj) % cols), (di, dj)) for (i, j), (di, dj) in blizzards
    ]

def initialize_graph(blizzards, rows, cols):
    period = rows * cols // gcd(rows, cols)
    reachable = defaultdict(set)
    busy_places = set(p for p, d in blizzards)
    valid_positions = set([(-1, 0), (rows, cols-1)] + [(i, j) for i in range(rows) for j in range(cols)])

    for t in range(period):
        blizzards = update_blizzards(blizzards, rows, cols)
        next_busy_places = set(p for p, d in blizzards)
        for i, j in valid_positions:
            if (i, j) not in busy_places:
                for di, dj in DIRECTIONS:
                    ni, nj = i + di, j + dj
                    if (ni, nj) in valid_positions and (ni, nj) not in next_busy_places:
                        reachable[(i, j, t)].add((ni, nj, (t+1) % period))
        busy_places = next_busy_places
    return reachable

def a_star(start, goal, neighbors, h):
    open_set = {start}

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)

    while open_set:
        current = min(open_set, key=f_score.__getitem__)
        if goal(current):
            return g_score[current]

        open_set.remove(current)
        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                fs = tentative_g_score + h(neighbor)
                if fs != inf:
                    f_score[neighbor] = fs
                open_set.add(neighbor)
    return None


def solve(reachable, rows, cols):    
    start = (-1, 0, 0)

    def is_goal(node):
        i, j, _ = node
        return i == rows and j == cols-1

    def h(node):
        i, j, _ = node
        return abs(rows - i) + abs(cols - j -1)
    
    def neighbors(node):
        return reachable[node]

    return a_star(start, is_goal, neighbors, h)


blizzards, rows, cols = parse(sys.stdin)
reachable = initialize_graph(blizzards, rows, cols)

print(solve(reachable, rows, cols))