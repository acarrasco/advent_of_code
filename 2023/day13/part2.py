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


def find_one_difference_indices(matrix_a, matrix_b):
    found_i = None
    found_j = None
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a[i])):
            if matrix_a[i][j] != matrix_b[i][j]:
                if found_i is not None:
                    return None, None
                else:
                    found_i = i
                    found_j = j
    return found_i, found_j

def find_horizontal_symmetry(problem):
    for i in range(1, len(problem)):
        rows = min(i, len(problem) - i)
        up = problem[i-rows:i]
        down = problem[i+rows-1:i-1:-1]
        di, dj = find_one_difference_indices(up, down)
        if di is not None:
            problem[i+di][dj] = {'.': '#', '#': '.'}[problem[i+di][dj]]
            return i
    return 0

def solve(problem):
    horizontal_symmetry = find_horizontal_symmetry(problem)
    problem = list(map(list, zip(*problem)))
    vertical_symmetry = find_horizontal_symmetry(problem)
    ## this should have been done, in case a change in vertical
    ## symmetry created a new horizontal symmetry xD
    # if horizontal_symmetry == 0 and vertical_symmetry > 0:
    #     problem = list(map(list, zip(*problem)))
    #     horizontal_symmetry = find_horizontal_symmetry(problem)

    return horizontal_symmetry * 100 + vertical_symmetry

print(sum(solve(problem) for problem in parse_input(sys.stdin.readlines())))
