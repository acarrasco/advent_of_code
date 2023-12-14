import sys

EMPTY = "."
FIXED_ROCK = "#"
MOVING_ROCK = "O"

def parse_input(lines):
    return list(list(line.strip()) for line in lines)

def tilt_north(problem):
    moved = True
    while moved:
        moved = False
        for up, bottom in zip(problem, problem[1:]):
            for j, (u, b) in enumerate(zip(up, bottom)):
                if u is EMPTY and b is MOVING_ROCK:
                    up[j] = MOVING_ROCK
                    bottom[j] = EMPTY
                    moved = True

def count_load(problem):
    n = len(problem)
    load = 0
    for i, row in enumerate(problem):
        south_rows = n - i
        load += sum(south_rows for x in row if x is MOVING_ROCK)
    return load

def solve(problem):
    tilt_north(problem)
    return count_load(problem)

print(solve(parse_input(sys.stdin.readlines())))