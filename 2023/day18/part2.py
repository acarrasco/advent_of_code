import sys
from collections import *
from itertools import *

DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'R': (0, 1),
    'L': (0, -1),
}

DigInstructions = namedtuple('DigInstructions', 'direction distance'.split())

def parse_line(line):
    _direction, _distance, color = line.split()
    distance = int(color[2:-2], 16)
    direction = 'RDLU'[int(color[-2])]
    return DigInstructions(DIRECTIONS[direction], distance)

def parse(lines):
    return [parse_line(line.strip()) for line in lines]

def get_vertices(steps):
    i, j = 0, 0
    coordinates = [(0, 0)]
    for (di, dj), distance in steps:
        i += di * distance
        j += dj * distance
        coordinates.append((i, j))
    return coordinates

def shoelace_formula(vertices):
    """
    Returns twice the area surrounded by vertices
    """
    edges = zip(vertices, vertices[1:])
    s = sum((bx - ax) * (by + ay) for (ax, ay), (bx, by) in edges)
    return abs(s)

def solve(problem):
    vertices = get_vertices(problem)
    perimeter = sum(distance for _, distance in problem)
    double_area = shoelace_formula(vertices)
    print(double_area, perimeter)
    return (double_area + perimeter) // 2 + 1 # off by one error U*_*

print(solve(parse(sys.stdin)))