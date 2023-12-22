import sys

NEIGHBORS = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
]

def reachable_in_steps(rows, cols, rocks, start, steps):
    def neighbors(node):
        i, j = node
        for di, dj in NEIGHBORS:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and (ni, nj) not in rocks:
                yield (ni, nj)

    reachable_in = {0: [start]}
    for step in range(1, steps+1):
        reachable_in[step] = set()
        for node in reachable_in[step-1]:
            for neighbor in neighbors(node):
                reachable_in[step].add(neighbor)
    return reachable_in[steps]

def parse(lines):
    rocks = set()
    for i, row in enumerate(lines):
        for j, v in enumerate(row):
            if v == '#':
                rocks.add((i, j))
            elif v == 'S':
                start = i, j
    size = (i+1, j+1)
    return rocks, size, start,

def print_garden(rows, cols, rocks, reachable):
    min_i = 0
    max_i = rows
    min_j = 0
    max_j = cols

    digits = max(len(str(max_j)), len(str(max_j)))
    col_headers = zip(*[str(j).rjust(digits+1) for j in range(min_j, max_j+1)])
    for line in col_headers:
        print(' '* (digits+2) +  ''.join(line))
    print()

    def get_char(i, j):
        if (i, j) in rocks:
             return '#'
        elif (i, j) in reachable:
             return 'O'
        else:
             return '.'

    for i in range(min_i, max_i+1):
        print(str(i).rjust(digits + 1), end=' ')
        print(''.join(get_char(i,j) for j in range(min_j, max_j+1)))

def solve(problem, steps=64):
    rocks, (rows, cols), start = problem
    reachable = reachable_in_steps(rows, cols, rocks, start, steps)
    print_garden(rows, cols, rocks, reachable)
    print()
    return len(reachable)

input = sys.stdin.readlines()
problem = parse(input)
print(solve(problem))