import sys

NEIGHBORS = [
    (-1, 0), (0, 1), (1, 0), (0, -1)
]

def parse(lines):
    return [[int(c) for c in line.strip()] for line in lines]

def valid_neighbors(height_map, height, i, j):
    for di, dj in NEIGHBORS:
        ni = i + di
        nj = j + dj
        if (0 <= ni < len(height_map) and 0 <= nj < len(height_map[ni])
            and height_map[ni][nj] == height + 1):
            yield ni, nj

def count_trailheads(height_map, i, j):
    height = height_map[i][j]
    if height == 9:
        return 1
    return sum(count_trailheads(height_map, ni, nj) for ni, nj in valid_neighbors(height_map, height, i, j))

def solve(problem):
    total = 0
    for i, row in enumerate(problem):
        for j, h in enumerate(row):
            if h == 0:
                c = count_trailheads(problem, i, j)
                print(i, j, c)
                total += c
    return total

print(solve(parse(sys.stdin)))