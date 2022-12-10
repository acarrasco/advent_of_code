import sys

COLUMNS = 40

def parse(line):
    tokens = line.strip().split()
    if len(tokens) == 1:
        return 1, 0
    else:
        return 2, int(tokens[1])

def solve(instructions):
    screen = []
    cycle = 0
    x = 0
    line = []
    for delay, value in instructions:
        for _ in range(delay):
            line.append('.#'[abs(x + 1 - (cycle % COLUMNS)) < 2])
            cycle += 1
            if cycle % COLUMNS == 0:
                screen.append(''.join(line))
                line = []
        x += value
    return '\n'.join(screen)

print(solve(map(parse, sys.stdin)))