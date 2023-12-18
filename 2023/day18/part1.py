import sys
from collections import *
from itertools import *

DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'R': (0, 1),
    'L': (0, -1),
}

DigInstructions = namedtuple('DigInstructions', 'direction distance color'.split())

def parse_line(line):
    direction, distance, color = line.split()
    return DigInstructions(DIRECTIONS[direction], int(distance), color[2:-1])

def parse(lines):
    return [parse_line(line.strip()) for line in lines]

def dig_trench(steps):
    i, j = 0, 0
    trench = set()

    for (di, dj), distance, _color in steps:
        for _ in range(distance):
            trench.add((i, j))
            i += di
            j += dj
    return trench

def flood_fill(bounds, inside_point, visited):
    if inside_point in bounds or inside_point in visited:
        return
    backtracking_stack = [inside_point]
    visited.add(inside_point)
    while backtracking_stack:
        i, j = backtracking_stack.pop()
        for di, dj in DIRECTIONS.values():
            candidate = i + di, j + dj
            if candidate not in bounds and candidate not in visited:
                visited.add(candidate)
                backtracking_stack.append(candidate)


class OutsideBounds:
    def __init__(self, points):
        self.min_row = min(i for i, j in points) - 1
        self.max_row = max(i for i, j in points) + 1
        self.min_col = min(j for i, j in points) - 1
        self.max_col = max(j for i, j in points) + 1

    def __contains__(self, point):
        i, j = point
        return i < self.min_row or i > self.max_row or j < self.min_col or j > self.max_col

def dig_interior(trench):
    outside_bounds = OutsideBounds(trench)
    surrounding_area = trench.copy()
    flood_fill(outside_bounds, (outside_bounds.min_row, outside_bounds.min_col), surrounding_area)
    surrounding_area -= trench
    inside_area = set()
    flood_fill(surrounding_area, (0, 0), inside_area)
    return inside_area


def solve(problem):
    trench = dig_trench(problem)
    interior = dig_interior(trench)
    return len(interior)

print(solve(parse(sys.stdin)))