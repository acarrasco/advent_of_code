import sys

ADYACENCY = [(-1,0), (1,0), (0,-1), (0,1)]

def parse(lines):
    return [[int(n) for n in line.strip()] for line in lines]

def score(trees, rows, columns, i, j):
    tree = trees[i][j]
    n = 1
    for di, dj in ADYACENCY:
        ni, nj = i + di, j + dj
        k = 0
        while 0 <= ni < rows and 0 <= nj < columns and trees[ni][nj] < tree:
            k += 1
            ni, nj = ni + di, nj + dj
        if 0 <= ni < rows and 0 <= nj < columns:
            k += 1
        n *= k
    return n

def solve(trees):
    rows = len(trees)
    columns = len(trees[0])
    return max(score(trees, rows, columns, i, j) for i in range(1, rows-1) for j in range(1, columns - 1))

print(solve(parse(sys.stdin)))