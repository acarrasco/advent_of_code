import sys
from pprint import pprint

FACE_DIRECTIONS = [
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (0, 0, -1),
    (0, -1, 0),
    (-1, 0, 0),
]

def parse(line):
    return tuple(map(int, line.strip().split(',')))

def solve(cubes):
    minx = min(x for x,y,z in cubes) - 1
    miny = min(y for x,y,z in cubes) - 1
    minz = min(z for x,y,z in cubes) - 1
    maxx = max(x for x,y,z in cubes) + 1
    maxy = max(y for x,y,z in cubes) + 1
    maxz = max(z for x,y,z in cubes) + 1

    def adjacent(x, y, z):
        for dx, dy, dz in FACE_DIRECTIONS:
            nx, ny, nz = x + dx, y + dy, z + dz
            if minx <= nx <= maxx and miny <= ny <= maxy and minz <= nz <= maxz:
                yield nx, ny, nz

    visible_faces = 0
    pending = set([(minx, miny, minz)])
    visited = set()
    while pending:
        next_pending = set()
        for p in pending:
            visited.add(p)
            for n in adjacent(*p):
                if n in visited:
                    continue
                if n in cubes:
                    visible_faces += 1
                else:
                    next_pending.add(n)
        pending = next_pending
    return visible_faces

print(solve(set(map(parse, sys.stdin))))