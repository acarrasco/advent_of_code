import sys
import collections

DIRECTIONS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]

def parse(lines):
    start = None
    end = None
    walls = set()
    for i, row in enumerate(lines):
        for j, c in enumerate(row.strip()):
            if c == 'S':
                start = i, j
            elif c == 'E':
                end = i, j
            elif c == '#':
                walls.add((i, j))
    return walls, start, end

def calculate_distances(walls, start, end):
    distances = {start: 0}
    pos = start
    while pos != end:
        i, j = pos
        for di, dj in DIRECTIONS:
            np = i + di, j + dj
            if np not in walls and np not in distances:
                distances[np] = distances[pos] + 1
                pos = np
                break
    return distances

def possible_cheats(distances):
    for p1 in distances:
        i1, j1 = p1
        for p2 in distances:
            i2, j2 = p2
            cartesian = abs(i2 - i1) + abs(j2 - j1)
            track = distances[p2] - distances[p1]
            gain = track - cartesian
            if gain > 2 and cartesian <= 20:
                yield gain

def solve(problem):
    walls, start, end = problem
    distances = calculate_distances(walls, start, end)
    cheat_counts = collections.Counter(possible_cheats(distances))
    return sum(v for k, v in cheat_counts.items() if k >= 100)

print(solve(parse(sys.stdin)))
