import sys
from collections import defaultdict

MOVEMENT = [
    (0, 1),
    (-1, 1),
    (1, 1),
]

def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0

def parse_points(line):
    points = line.split('->')
    for point in points:
        x, y = point.strip().split(',')
        yield int(x), int(y)

def parse(lines):
    cave = defaultdict(int)
    for line in lines:
        points = list(parse_points(line))
        for (a_x, a_y), (b_x, b_y) in zip(points, points[1:]):
            d_x, d_y = sign(a_x - b_x), sign(a_y - b_y)
            p_x, p_y = a_x, a_y
            while p_x != b_x or p_y != b_y:
                cave[p_x,p_y] = 1
                p_x -= d_x
                p_y -= d_y
        cave[p_x, p_y] = 1
    bottom = max(p[1] for p in cave)
    return cave, bottom

def simulate_turn(cave, bottom):
    p_x, p_y = 500, 0
    while p_y < bottom:
        for d_x, d_y in MOVEMENT:
            if not cave[p_x + d_x, p_y + d_y]:
                p_x, p_y = p_x + d_x, p_y + d_y
                break
        else:
            cave[p_x, p_y] = 2
            return False
    return True
    

def solve(cave, bottom):
    turns = 0
    while not simulate_turn(cave, bottom):
        turns += 1
    return turns


print(solve(*parse(sys.stdin)))