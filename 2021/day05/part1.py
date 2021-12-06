import sys
import pprint
from collections import defaultdict


def parse_coordinates(coord):
    x, y = coord.split(',')
    return int(x), int(y)


def parse_lines(lines):
    for line in lines:
        left, right = line.split('->')
        yield parse_coordinates(left), parse_coordinates(right)


def interpolate(vector):
    (x0, y0), (x1, y1) = vector
    dx = x1 - x0
    dy = y1 - y0
    magnitude = max(abs(dx), abs(dy))
    xmov = dx and dx/abs(dx) or 0
    ymov = dy and dy/abs(dy) or 0
    if xmov and ymov:
        return []
    return [(x0 + xmov * n, y0 + ymov * n) for n in range(magnitude + 1)]


def find_overlapping(vectors, threshold=2):
    overlapping = set()
    m = defaultdict(int)
    for vector in vectors:
        for coordinate in interpolate(vector):
            m[coordinate] += 1
            if m[coordinate] >= threshold:
                overlapping.add(coordinate)
    return overlapping

print(len(find_overlapping(parse_lines(sys.stdin.readlines()))))