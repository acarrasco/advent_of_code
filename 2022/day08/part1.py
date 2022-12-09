import sys
import numpy

def parse(lines):
    return numpy.array([[int(n) for n in line.strip()] for line in lines])

def solve(trees):
    rows = len(trees)
    columns = len(trees[0])
    
    n = 0
    for i in range(1, rows-1):
        for j in range(1, columns-1):
            tree = trees[i][j]
            n += (
                (trees[:i, j]   < tree).all() or
                (trees[i+1:, j] < tree).all() or
                (trees[i, :j]   < tree).all() or
                (trees[i, j+1:] < tree).all()
            )
    return n + 2 * (rows + columns) - 4

print(solve(parse(sys.stdin)))