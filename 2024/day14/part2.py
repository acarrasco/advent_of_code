import sys
import argparse
from collections import Counter

def parse_line(line):
    p, v = line.split()
    px, py = p[2:].split(',')
    vx, vy = v[2:].split(',')

    return (int(px), int(py)), (int(vx), int(vy))

def simulate(robot, rows, cols, turns):
    (px, py), (vx, vy) = robot
    return (px + vx * turns) % cols, (py + vy * turns) % rows

def parse(lines):
    return [parse_line(line) for line in lines]

def print_robots(rows, cols, robot_positions):
    coords = Counter(robot_positions)
    
    for y in range(rows):
        print(''.join(str(coords.get((x, y), '.')) for x in range(cols)))

NEIGHBORS = [
    (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
]

def explore_robots(robots, seen, x, y):
    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        seen.add((x, y))
        for dx, dy in NEIGHBORS:
            nx, ny = x + dx, y + dy
            if (nx, ny) in robots and (nx, ny) not in seen:
                stack.append((nx, ny))
    return seen

def candidate(positions):
    ps = set(positions)
    majority = len(positions) // 3
    seen = set()
    for x, y in ps:
        if (x, y) not in seen:
            new_seen = explore_robots(ps, set(), x, y)
            if len(new_seen) >= majority:
                return True
            seen.update(new_seen)
            if len(seen) > majority:
                return False
    return False

def solve(problem, rows, cols):
    t = 0
    while True:
        positions = [simulate(robot, rows, cols, t) for robot in problem]
        if candidate(positions):
            print_robots(rows, cols, positions)
            print()
            return t
        t += 1


parser = argparse.ArgumentParser()
parser.add_argument('--turns', default=100, type=int)
parser.add_argument('--rows', default=103, type=int)
parser.add_argument('--cols', default=101, type=int)

args = parser.parse_args()

print(solve(parse(sys.stdin), args.rows, args.cols))