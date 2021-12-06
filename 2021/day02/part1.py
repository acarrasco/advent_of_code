import sys

coordinates_mapping = {
    'forward': ('x', 1),
    'backward': ('x', -1),
    'up': ('y', -1),
    'down': ('y', 1)
}

directions_and_distances = (line.strip().split() for line in sys.stdin.readlines())

position = {
    'x': 0,
    'y': 0,
}

for direction, distance in directions_and_distances:
    coordinate, multiplier = coordinates_mapping[direction]
    position[coordinate] += int(distance) * multiplier

print(position['x'] * position['y'])
