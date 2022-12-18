import sys

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
    seen = set()
    visible_faces = 0
    for cube in cubes:
        x, y, z = cube
        seen.add(cube)
        for dx, dy, dz in FACE_DIRECTIONS:
            if (x + dx, y + dy, z + dz) in seen:
                visible_faces -= 1
            else:
                visible_faces += 1
    return visible_faces

print(solve(map(parse, sys.stdin)))