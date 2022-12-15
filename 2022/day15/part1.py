import sys
import re

LINE_EXP = 'Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)'

def parse(line):
    m = re.match(LINE_EXP, line.strip())
    return tuple(map(int, m.groups()))

def solve(sensors_and_beacons, row):
    beacons_in_row = set()
    excluded = set()
    for sx, sy, bx, by in sensors_and_beacons:
        beacon_distance = abs(sx - bx) + abs(sy - by)
        row_distance = abs(sy - row)
        if row_distance <= beacon_distance:
            for dx in range(beacon_distance - row_distance + 1):
                excluded.add(sx + dx)
                excluded.add(sx - dx)
        if by == row:
            beacons_in_row.add(bx)
    
    return len(excluded - beacons_in_row)
        

print(solve(map(parse, sys.stdin), 2000000))