import sys

ROTATE_RIGHT = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}

def parse(lines):
    return [line.strip() for line in lines]

def step(obstacles, n, m, position, direction):
    i, j = position
    di, dj = direction
    ni, nj = i + di, j + dj
    if 0 <= ni < n and 0 <= nj < m:
        if obstacles[ni][nj] == '#':
            direction = ROTATE_RIGHT[direction]
            di, dj = direction
            ni, nj = i + di, j + dj

    return (ni, nj), direction

def find_start(obstacles):
    for i, row in enumerate(obstacles):
        for j, cell in enumerate(row):
            if cell == '^':
                return i, j

def solve(obstacles):
    n, m = len(obstacles), len(obstacles[0])
    position = find_start(obstacles)
    direction = (-1, 0)
    positions = {position}
    while True:
        position, direction = step(obstacles, n, m, position, direction)
        print(position, direction)
        i, j = position
        if not(0 <= i < n and 0 <= j < m):
            return len(positions)
        positions.add(position)

print(solve(parse(sys.stdin)))
