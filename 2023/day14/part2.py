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

def tilt_south(problem):
    moved = True
    while moved:
        moved = False
        for up, bottom in zip(problem, problem[1:]):
            for j, (u, b) in enumerate(zip(up, bottom)):
                if u is MOVING_ROCK and b is EMPTY:
                    up[j] = EMPTY
                    bottom[j] = MOVING_ROCK
                    moved = True

def tilt_west(problem):
    moved = True
    while moved:
        moved = False
        for row in problem:
            for j, x in enumerate(row[1:], 1):
                if x is MOVING_ROCK and row[j-1] is EMPTY:
                    row[j-1] = MOVING_ROCK
                    row[j] = EMPTY
                    moved = True

def tilt_east(problem):
    moved = True
    while moved:
        moved = False
        for row in problem:
            for j, x in enumerate(row[1:], 1):
                if x is EMPTY and row[j-1] is MOVING_ROCK:
                    row[j-1] = EMPTY
                    row[j] = MOVING_ROCK
                    moved = True

def tilt(problem):
    tilt_north(problem)
    tilt_west(problem)
    tilt_south(problem)
    tilt_east(problem)

def count_load(problem):
    n = len(problem)
    load = 0
    for i, row in enumerate(problem):
        south_rows = n - i
        load += sum(south_rows for x in row if x is MOVING_ROCK)
    return load

def problem_to_hashable(problem):
    return tuple("".join(row) for row in problem)

TARGET_CYCLES = 1000000000
def solve(problem):
    cycles = {}
    for i in range(TARGET_CYCLES):
        tilt(problem)
        hashed_problem = problem_to_hashable(problem)
        if hashed_problem in cycles:
            break
        cycles[hashed_problem] = i

    cycle_start = cycles[hashed_problem]
    cycle_length = i - cycle_start
    remaining_cycles = TARGET_CYCLES - i - 1
    remainder_cycles = cycle_start + (remaining_cycles % cycle_length)
    hashed_in_remainder_cycles = next(k for k, v in cycles.items() if v == remainder_cycles)
    problem_in_target_cycle = parse_input(hashed_in_remainder_cycles)
    return count_load(problem_in_target_cycle)

problem = parse_input(sys.stdin.readlines())
print(solve(problem))