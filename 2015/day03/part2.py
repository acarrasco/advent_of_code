import sys

movements = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, 1),
    'v': (0, -1),
}

visited = set([(0, 0)])
is_santa = True
positions = {
    True: (0, 0),
    False: (1, 1)
}

for movement in sys.stdin.read():
    dx, dy = movements.get(movement, (0, 0))
    x, y = positions[is_santa]
    new_position = x + dx, y + dy
    positions[is_santa] = new_position
    visited.add(new_position)
    is_santa = not is_santa

print(len(visited))