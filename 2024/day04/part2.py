import sys

PATTERNS = [
    [(-1,-1), (0, 0), (1, 1)],
    [(-1, 1), (0, 0), (1, -1)],
]

def get_string(puzzle, coordinates, i, j):
    n, m = len(puzzle), len(puzzle[0])
    s = ''
    for di, dj in coordinates:
        ni = i + di
        nj = j + dj
        if 0 <= ni < n and 0 <= nj < m:
            s += puzzle[ni][nj]
        else:
            return ''

    return s

def get_patterns(puzzle, i, j):
    for p in PATTERNS:
        yield get_string(puzzle, p, i, j)

def parse(lines):
    return [line.strip() for line in lines]

def solve(problem):
    WORDS = ('MAS', 'SAM')
    result = 0
    for i in range(len(problem)):
        for j in range(len(problem[0])):
            if all(p in WORDS for p in get_patterns(problem, i, j)):
                result += 1
    return result

print(solve(parse(sys.stdin)))