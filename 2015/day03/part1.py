import sys

movements = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, 1),
    'v': (0, -1),
}

visited = set([(0, 0)])
x, y = 0, 0

for movement in sys.stdin.read():
    dx, dy = movements.get(movement, (0, 0))
    x += dx
    y += dy
    visited.add((x, y))

print(len(visited))