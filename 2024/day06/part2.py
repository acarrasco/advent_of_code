import sys

ROTATE_RIGHT = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}

OBSTACLE = '#'

def parse(lines):
    return [line.strip() for line in lines if line.strip()]

def step(obstacles, n, m, position, direction):
    i, j = position
    di, dj = direction
    ni, nj = i + di, j + dj
    while 0 <= ni < n and 0 <= nj < m and obstacles[ni][nj] == OBSTACLE:
        direction = ROTATE_RIGHT[direction]
        di, dj = direction
        ni, nj = i + di, j + dj

    return (ni, nj), direction

def find_start(obstacles):
    for i, row in enumerate(obstacles):
        for j, cell in enumerate(row):
            if cell == '^':
                return i, j

def traverse(obstacles, n, m, start):
    position = start
    direction = (-1, 0)
    seen_positions_and_directions = {(position, direction)}
    path = [position]
    while True:
        position, direction = step(obstacles, n, m, position, direction)
        if (position, direction) in seen_positions_and_directions:
            return path, True
        i, j = position
        if not(0 <= i < n and 0 <= j < m):
            return path, False
        seen_positions_and_directions.add((position, direction))
        path.append(position)

def add_obstacle(obstacles, i, j):
    obstacles_copy = [list(row) or row for ri, row in enumerate(obstacles)]
    obstacles_copy[i][j] = OBSTACLE
    return obstacles_copy

def solve(obstacles):
    loops = 0
    n, m = len(obstacles), len(obstacles[0])
    start = find_start(obstacles)
    original_path, _ = traverse(obstacles, n, m, start)
    candidates = set(original_path)
    loops = 0
    for i, j in sorted(candidates):
        if obstacles[i][j] == '.':
            with_new_obstacle = add_obstacle(obstacles, i, j)
            visited, is_loop = traverse(with_new_obstacle, n, m, start)
            if is_loop:
                loops += 1
    return loops

print(solve(parse(sys.stdin)))