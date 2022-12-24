import sys
from collections import defaultdict
from pprint import pprint

def parse(lines):
    elves = set()
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '#':
                elves.add((i, j))
    return elves

POINTS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

ADJACENCY = [
    (i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j
]

SCAN_AREA = {
    (-1, 0): ((-1, 0), (-1, 1), (-1, -1)),
    (1, 0): ((1, 0), (1, 1), (1, -1)),
    (0, -1): ((0, -1), (1, -1), (-1, -1)),
    (0, 1): ((0, 1), (1, 1), (-1, 1)),
}

def simulate(elves, turn):
    proposed = defaultdict(list)
    result = set()
    for i, j in elves:
        if all((i + di, j + dj) not in elves for di, dj in ADJACENCY):
            result.add((i, j))
            continue
        for k in range(4):
            orientation = POINTS[(turn + k) % 4]
            if all((i + scan_di, j + scan_dj) not in elves for scan_di, scan_dj in SCAN_AREA[orientation]):
                di, dj = orientation
                proposed[i + di, j + dj].append((i, j))
                break
        else:
            result.add((i, j))

    if len(result) == len(elves):
        return None

    for destination, sources in proposed.items():
        if len(sources) == 1:
            result.add(destination)
        else:
            result.update(sources)

    return result

def run_simulation(elves):
    turn = 0
    while elves:
        elves = simulate(elves, turn)
        turn += 1
    return turn

def print_area(elves):
    min_i = min(i for i,j in elves)
    max_i = max(i for i,j in elves)
    min_j = min(j for i,j in elves)
    max_j = max(j for i,j in elves)

    digits = max(len(str(max_j)), len(str(max_j)))
    col_headers = zip(*[str(j).rjust(digits+1) for j in range(min_j, max_j+1)])
    for line in col_headers:
        print(' '* (digits+2) +  ''.join(line))
    print()

    for i in range(min_i, max_i+1):
        print(str(i).rjust(digits + 1), end=' ')
        print(''.join('#' if (i, j) in elves else '.' for j in range(min_j, max_j+1)))


print(run_simulation(parse(sys.stdin)))
