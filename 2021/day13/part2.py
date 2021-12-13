import sys
import itertools
from collections import defaultdict
from pprint import pprint


def parse_line(line):
    a, b = line.strip().split(',')
    return int(a), int(b)


def parse_fold(line):
    _, axis_value = line.rsplit(' ', 1)
    axis, value = axis_value.split('=')
    return axis, int(value)


def not_empty(s):
    return s.strip()


def parse(lines):
    line_it = map(str.strip, lines)
    points_lines = itertools.takewhile(not_empty, line_it)
    points = list(map(parse_line, points_lines))
    folds = list(map(parse_fold, line_it))
    return points, folds


def do_fold(points, fold):
    axis, fold_distance = fold
    result = set()
    for x, y in points:
        nx, ny = x, y
        if axis == 'x' and x > fold_distance:
            nx = 2*fold_distance - x
        elif axis == 'y' and y > fold_distance:
            ny = 2*fold_distance - y

        result.add((nx, ny))
    return result


def print_points(points):
    w, _ = max(points)
    _, h = max(points, key=lambda p: p[1])
    for y in range(h+1):
        print(''.join((x, y) in points and '#' or '.' for x in range(w+1)))


def solve(points, folds):
    for fold in folds:
        points = do_fold(points, fold)
    return points


input = sys.stdin


points, folds = parse(input)

print_points(solve(points, folds))
