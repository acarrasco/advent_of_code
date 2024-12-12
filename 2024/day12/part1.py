import sys
import itertools

NEIGHBORS = [
    [-1, 0],
    [0, 1],
    [1, 0],
    [0, -1],
]

def parse(lines):
    return [line.strip() for line in lines]

def calculate_area_and_perimeter(problem, n, m, c, i, j, current_area, current_perimeter):
    for di, dj in NEIGHBORS:
        ni = i + di
        nj = j + dj
        if 0 <= ni < n and 0 <= nj < m and problem[ni][nj] == c:
            current_perimeter[0] -= 1
            if (ni, nj) not in current_area:
                current_area.add((ni, nj))
                current_perimeter[0] += 4
                calculate_area_and_perimeter(problem, n, m, c, ni, nj, current_area, current_perimeter)

def solve(problem):
    visited = set()
    total = 0
    n = len(problem)
    m = len(problem[0])
    for i, row in enumerate(problem):
        for j, c in enumerate(row):
            if (i, j) not in visited:
                area = {(i, j)}
                perimeter = [4]
                calculate_area_and_perimeter(problem, n, m, c, i, j, area, perimeter)
                visited.update(area)
                total += len(area) * perimeter[0]
    return total

print(solve(parse(sys.stdin)))