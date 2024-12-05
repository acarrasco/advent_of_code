import sys

DIRECTIONS = [
    (di, dj) for di in (-1, 0, 1) for dj in (-1, 0, 1) if di or dj
]

def get_string(puzzle, length, i, j, direction):
    n, m = len(puzzle), len(puzzle[0])
    di, dj = direction
    s = ''
    while len(s) < length and 0 <= i < n and 0 <= j < m:
        s += puzzle[i][j]
        i += di
        j += dj

    if len(s) == length:
        return s
    else:
        return ''

def parse(lines):
    return [line.strip() for line in lines]

def solve(problem):
    WORD = 'XMAS'
    lenght = len(WORD)
    result = 0
    for i in range(len(problem)):
        for j in range(len(problem[0])):
            for direction in DIRECTIONS:
                if get_string(problem, lenght, i, j, direction) == WORD:
                    result += 1
    return result

print(solve(parse(sys.stdin)))