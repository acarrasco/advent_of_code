import sys
from pprint import pprint

def parse_input(lines):
    current_block = []
    for line in lines:
        if line.strip() == "":
            yield current_block
            current_block = []
        else:
            current_block.append(list(line.strip()))
    yield current_block


def has_one_difference(matrix_a, matrix_b):
    found = False
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a[i])):
            if matrix_a[i][j] != matrix_b[i][j]:
                if found:
                    return False
                else:
                    found = True
    return found

def find_horizontal_symmetry(problem):
    for i in range(1, len(problem)):
        rows = min(i, len(problem) - i)
        up = problem[i-rows:i]
        down = problem[i+rows-1:i-1:-1]
        if has_one_difference(up, down):
            return i
    return 0

def solve(problem):
    horizontal_symmetry = find_horizontal_symmetry(problem)

    return horizontal_symmetry * 100 or find_horizontal_symmetry(list(zip(*problem)))

print(sum(solve(problem) for problem in parse_input(sys.stdin.readlines())))
