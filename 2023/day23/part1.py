import sys
from collections import defaultdict

SLOPES = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0),
}
ROCK = '#'
PATH = '.'

def parse(lines):
    return [line.strip() for line in lines if line.strip()]

def neighbors(maze, point):
    i, j = point
    for s, (di, dj) in SLOPES.items():
        ni, nj = i + di, j + dj
        if 0 <= ni < len(maze) and 0 <= nj < len(maze[0]) and maze[ni][nj] in (PATH, s):
            yield ni, nj

def calculate_paths_from(maze, coming_from, start, explored_paths):
    d = 0
    previous = coming_from
    next_point = start
    while len(next_points := set(neighbors(maze, next_point)) - {previous}) == 1:
        d += 1
        previous = next_point
        next_point, = next_points
    if d > 0 and next_point not in explored_paths[coming_from]:
        explored_paths[coming_from][next_point] = d
        for nnp in next_points:
            calculate_paths_from(maze, next_point, nnp, explored_paths)

def paths_length(paths, exit_row, point, visited, distance):
    i, j = point
    if i == exit_row:
        yield distance
        return
    for next_point in paths[point]:
        if next_point not in visited:
            next_visited = visited | {next_point}
            next_distance = 1 + distance + paths[point][next_point]
            yield from paths_length(paths, exit_row, next_point, next_visited, next_distance)


def solve(maze):
    paths = defaultdict(dict)
    calculate_paths_from(maze, (-1, 1), (0, 1), paths)
    return max(paths_length(paths, len(maze)-1, (-1, 1), {(-1, 1)}, -1))


lines = sys.stdin.readlines()
print(solve(parse(lines)))