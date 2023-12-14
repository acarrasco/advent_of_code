import sys
from collections import defaultdict

EMPTY = "."
FIXED_ROCK = "#"
MOVING_ROCK = "O"

def parse_input(lines):
    lines = [line.strip() for line in lines if line.strip()]

    fixed_rocks = defaultdict(list)
    moving_rocks = defaultdict(list)
    for i, line in enumerate(lines):
        for j, x in enumerate(line):
            if x is FIXED_ROCK:
                fixed_rocks[i].append(j)
            elif x is MOVING_ROCK:
                moving_rocks[i].append(j)
    return fixed_rocks, moving_rocks, len(lines), len(lines[0])

def tilt_north(fixed_rocks, moving_rocks):
    result = defaultdict(list)
    max_north_clearance = defaultdict(lambda: -1)
    upper_row_with_fixed_rocks = min(fixed_rocks, default=0)
    for col in fixed_rocks[upper_row_with_fixed_rocks]:
        max_north_clearance[col] = upper_row_with_fixed_rocks

    all_rows = set(fixed_rocks.keys()) | set(moving_rocks.keys())

    for row in sorted(all_rows):
        for col in moving_rocks.get(row, ()):
            destination_row = max_north_clearance[col] + 1
            result[destination_row].append(col)
            max_north_clearance[col] = destination_row
        for col in fixed_rocks.get(row, ()):
            max_north_clearance[col] = row
    return result

def rotate_90_clockwise(sparse_matrix, rows, cols):
    result = defaultdict(list)
    for i in sparse_matrix:
        for j in sparse_matrix[i]:
            result[j].append(rows - i - 1)
    return result, cols, rows

def tilt_and_rotate_360(fixed_rocks_by_orientation, moving_rocks, rows, cols):
    for fixed_rocks in fixed_rocks_by_orientation:
        moving_rocks = tilt_north(fixed_rocks, moving_rocks)
        moving_rocks, rows, cols = rotate_90_clockwise(moving_rocks, rows, cols)

    return moving_rocks

def calculate_load(moving_rocks, rows):
    load = 0
    for row in moving_rocks:
        south_rows = rows - row
        load += south_rows * len(moving_rocks[row])
    return load

def sparse_to_hashable(sparse_matrix):
    def row_to_hashable(row):
        return f'{row}:{",".join(map(str, sparse_matrix[row]))}'
    return ';'.join(row_to_hashable(row) for row in sorted(sparse_matrix))

def hashable_to_sparse(hashable):
    sparse_matrix = defaultdict(list)
    for row in hashable.split(';'):
        row, cols = row.split(':')
        sparse_matrix[int(row)] = list(map(int, cols.split(',')))
    return sparse_matrix

def problem_to_input(fixed_rocks, moving_rocks, rows, cols):
    out = []
    def get_char(i, j):
        if i in moving_rocks and j in moving_rocks[i]:
            return MOVING_ROCK
        if i in fixed_rocks and j in fixed_rocks[i]:
            return FIXED_ROCK
        return EMPTY
    for i in range(rows):
        out.append(''.join(get_char(i,j) for j in range(cols)))
    return '\n'.join(out)

def calculate_fixed_rocks_rotations(fixed_rocks, rows, cols):
    fixed_rocks_by_orientation = [fixed_rocks]
    for _ in range(3):
        fixed_rocks, rows, cols = rotate_90_clockwise(fixed_rocks, rows, cols)
        fixed_rocks_by_orientation.append(fixed_rocks)
    return fixed_rocks_by_orientation

def solve(fixed_rocks, moving_rocks, rows, cols):
    TARGET_CYCLES = 1000000000

    fixed_rocks_by_orientation = calculate_fixed_rocks_rotations(fixed_rocks, rows, cols)
    cycles = {}
    for i in range(TARGET_CYCLES):
        moving_rocks = tilt_and_rotate_360(fixed_rocks_by_orientation, moving_rocks, rows, cols)
        hashed_moving_rocks = sparse_to_hashable(moving_rocks)
        if hashed_moving_rocks in cycles:
            break
        cycles[hashed_moving_rocks] = i

    cycle_start = cycles[hashed_moving_rocks]
    cycle_length = i - cycle_start
    remaining_cycles = TARGET_CYCLES - i - 1 # -1 because we started counting from 0
    remainder_cycles = cycle_start + (remaining_cycles % cycle_length)
    hashed_in_remainder_cycles = next(k for k, v in cycles.items() if v == remainder_cycles)
    moving_rocks_in_target_cycle = hashable_to_sparse(hashed_in_remainder_cycles)
    return calculate_load(moving_rocks_in_target_cycle, rows)

problem = parse_input(sys.stdin.readlines())
print(solve(*problem))