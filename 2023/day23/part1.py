import sys

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

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

def explore_maze(maze, i, j, visited):
    if i == len(maze) - 1:
        yield len(visited)
        return

    for s, (di, dj) in SLOPES.items():
        ni, nj = i + di, j + dj
        if (0 <= ni < len(maze) and
            0 <= nj < len(maze[0]) and
            maze[ni][nj] != ROCK and
            (ni, nj) not in visited):
                v = maze[ni][nj]
                new_visited = set(visited)
                new_visited.add((ni, nj))
                if v == PATH:
                    yield from explore_maze(maze, ni, nj, new_visited)
                elif v == s:
                    yield from explore_maze(maze, ni, nj, new_visited)

def solve(problem):
    return max(explore_maze(problem, 0, 1, []))

lines = sys.stdin.readlines()
print(solve(parse(lines)))