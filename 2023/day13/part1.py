import sys

def parse_input(lines):
    current_block = []
    for line in lines:
        if line.strip() == "":
            yield current_block
            current_block = []
        else:
            current_block.append(line.strip())
    yield current_block


def find_horizontal_symmetry(problem):
    for i in range(1, len(problem)):
        rows = min(i, len(problem) - i)
        up = problem[i-rows:i]
        down = problem[i+rows-1:i-1:-1]
        if up == down:
            return i
    return 0

def solve(problem):
    horizontal_symmetry = find_horizontal_symmetry(problem)
    vertical_symmetry = find_horizontal_symmetry(list(zip(*problem)))

    return horizontal_symmetry * 100 + vertical_symmetry

print(sum(solve(problem) for problem in parse_input(sys.stdin.readlines())))
