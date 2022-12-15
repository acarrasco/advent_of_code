import sys
import re

LINE_EXP = 'Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)'

MAX_COORDINATE = 4000000

def parse(line):
    m = re.match(LINE_EXP, line.strip())
    return tuple(map(int, m.groups()))

def possible(sensors_and_beacons, p):
    px, py = p
    for sx, sy, bx, by in sensors_and_beacons:
        dsb = abs(sx - bx) + abs(sy - by)
        dsp = abs(sx - px) + abs(sy - py)
        if dsp <= dsb:
            return False
    return True

def boundaries(p, d):
    px, py = p
    for dx in range(d + 1):
        dy = d - dx
        if 0 < px + dx < MAX_COORDINATE and 0 < py + dy < MAX_COORDINATE:
            yield px + dx, py + dy
        if 0 < px - dx < MAX_COORDINATE and 0 < py + dy < MAX_COORDINATE:
            yield px - dx, py + dy
        if 0 < px + dx < MAX_COORDINATE and 0 < py - dy < MAX_COORDINATE:
            yield px + dx, py - dy
        if 0 < px - dx < MAX_COORDINATE and 0 < py - dy < MAX_COORDINATE:
            yield px - dx, py - dy

def solve(sensors_and_beacons):
    for sx, sy, bx, by in sensors_and_beacons:
        d = abs(sx - bx) + abs(sy - by)
        for p in boundaries((sx, sy), d + 1):
            if possible(sensors_and_beacons, p):
                return p
    return

def format(p):
    px, py = p
    return px * MAX_COORDINATE + py

print(format(solve(list(map(parse, sys.stdin)))))
