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

def points_at_distance(p, distance):
    i, j = p

    yield i + distance, j
    yield i - distance, j
    yield i, j + distance
    yield i, j - distance

    for k in range(1, distance):
        ck = distance - k
        yield i + k, j + ck
        yield i + k, j - ck
        yield i - k, j + ck
        yield i - k, j - ck

def possible_cheats(distances, max_cheat, count_threshold):
    for p1 in distances:
        for cartesian in range(2, max_cheat+1):
            for p2 in points_at_distance(p1, cartesian):
                if p2 in distances:
                    track = distances[p2] - distances[p1]
                    gain = track - cartesian
                    if gain >= count_threshold:
                        yield 1

def solve(problem, max_cheat=20, count_threshold=100):
    walls, start, end = problem
    distances = calculate_distances(walls, start, end)
    return sum(possible_cheats(distances, max_cheat, count_threshold))

print(solve(parse(sys.stdin)))
