import sys

import numpy

SIZE = 1000
grid = numpy.ndarray(shape=(SIZE, SIZE), dtype=int)
grid.fill(False)


def turn_on(region):
    grid[region] += 1


def turn_off(region):
    grid[region] -= 1
    grid[region][grid[region] < 0] = 0


def toggle(region):
    grid[region] += 2


def parse_range(r, extra=0):
    return map(lambda x: int(x) + extra, r.split(','))


def parse_command(line):
    left, range_end = line.split(' through ')
    action, range_start = left.rsplit(' ', 1)
    return action, parse_range(range_start), parse_range(range_end, 1)


actions = {
    'turn on': turn_on,
    'turn off': turn_off,
    'toggle': toggle,
}

commands = map(parse_command, sys.stdin.readlines())
for action, range_start, range_end in commands:
    x0, y0 = range_start
    x1, y1 = range_end
    actions[action]((slice(x0, x1), slice(y0, y1)))

print(grid.sum())
