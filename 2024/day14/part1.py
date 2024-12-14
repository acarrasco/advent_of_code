import sys
import argparse


def get_regions(rows, cols):
    return [
        ((0, 0), (cols//2, rows//2)),
        ((0, rows//2+1), (cols//2, rows)),
        ((cols//2+1, 0), (cols, rows//2)),
        ((cols//2+1, rows//2+1), (cols, rows)),
    ]

def parse_line(line):
    p, v = line.split()
    px, py = p[2:].split(',')
    vx, vy = v[2:].split(',')

    return (int(px), int(py)), (int(vx), int(vy))

def simulate(robot, rows, cols, turns):
    (px, py), (vx, vy) = robot
    return (px + vx * turns) % cols, (py + vy * turns) % rows

def count_in_region(region, robot_positions):
    count = 0
    (rx0, ry0), (rx1, ry1) = region
    for x, y in robot_positions:
        if rx0 <= x < rx1 and ry0 <= y < ry1:
            count += 1
    return count

def parse(lines):
    return [parse_line(line) for line in lines]

def print_robots(rows, cols, robot_positions):
    from collections import Counter
    coords = Counter(robot_positions)
    
    for y in range(rows):
        print(''.join(str(coords.get((x, y), '.')) for x in range(cols)))

def solve(problem, rows, cols, turns):
    positions = [simulate(robot, rows, cols, turns) for robot in problem]
    print_robots(rows, cols, positions)
    print(get_regions(rows, cols))
    regions = [count_in_region(r, positions) for r in get_regions(rows, cols)]
    print(regions)
    result = 1
    for rc in regions:
        result *= rc
    return result

parser = argparse.ArgumentParser()
parser.add_argument('--turns', default=100, type=int)
parser.add_argument('--rows', default=103, type=int)
parser.add_argument('--cols', default=101, type=int)

args = parser.parse_args()

print(solve(parse(sys.stdin), args.rows, args.cols, args.turns))