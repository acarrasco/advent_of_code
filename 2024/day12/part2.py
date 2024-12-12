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

def calculate_area(problem, n, m, c, i, j, current_area):
    for di, dj in NEIGHBORS:
        ni = i + di
        nj = j + dj
        if 0 <= ni < n and 0 <= nj < m and problem[ni][nj] == c:
            if (ni, nj) not in current_area:
                current_area.add((ni, nj))
                calculate_area(problem, n, m, c, ni, nj, current_area)

def calculate_row_sides(area):
    rows = {i for i, _ in area}
    cols = sorted({j for _, j in area})
    sides = 0
    rows = sorted(rows | {i + 1 for i in rows} | {i - 1 for i in rows})
    for i in rows:
        pj = None
        pup = None
        for j in cols:
            up = (i-1, j) in area
            down = (i, j) in area
            if up != down:
                if pj != j - 1 or pup != up:
                    sides += 1
                pup = up
                pj = j
    return sides

def solve(problem):
    visited = set()
    total = 0
    n = len(problem)
    m = len(problem[0])
    for i, row in enumerate(problem):
        for j, c in enumerate(row):
            if (i, j) not in visited:
                area = {(i, j)}
                calculate_area(problem, n, m, c, i, j, area)
                sides = calculate_row_sides(area) + calculate_row_sides({(j, i) for i, j in area})
                visited.update(area)
                total += len(area) * sides
    return total

print(solve(parse(sys.stdin)))