import sys
import argparse

DIRECTIONS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]

def parse_line(line):
    j, i = [int(x) for x in line.split(',')]
    return i, j

def parse(lines):
    return [parse_line(line) for line in lines]

def connected(start, end, rows, cols, walls):
    pending = [start]
    seen = set()
    while pending:
        p = pending.pop()
        if p == end:
            return True

        i, j = p
        for di, dj in DIRECTIONS:
            ni = i + di
            nj = j + dj
            np = ni, nj

            if 0 <= ni < rows and 0 <= nj < cols and np not in walls and np not in seen:
                seen.add(np)
                pending.append(np)

    return False

def solve(problem, fallen_bytes, rows, cols):
    end = rows-1, cols-1

    walls = set(b for _, b in zip(range(fallen_bytes), problem))
    for i in range(fallen_bytes, len(problem)):
        walls.add(problem[i])
        if not connected((0, 0), end, rows, cols, walls):
            y, x = problem[i]
            return f'{x},{y}'

parser = argparse.ArgumentParser()
parser.add_argument('--bytes', type=int, default=1024)
parser.add_argument('--rows', type=int, default=71)
parser.add_argument('--cols', type=int, default=71)
args = parser.parse_args()

print(solve(parse(sys.stdin), args.bytes, args.rows, args.cols))
