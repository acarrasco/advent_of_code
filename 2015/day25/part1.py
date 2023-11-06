import sys
import re

SEED = 20151125
MULTIPLIER = 252533
DIVISOR = 33554393

row, column = map(int, re.findall('([\d]+)', sys.stdin.read()))

def next_coordinates(i, j):
    if i == 1:
        return j+1, 1
    else:
        return i-1, j+1

def generate_coordinates():
    i, j = 1, 1
    while True:
        yield i, j
        i, j = next_coordinates(i, j)

def solve(row, column):
    n = SEED
    for i, j in generate_coordinates():
        if i == row and j == column:
            return n
        n = (n * MULTIPLIER) % DIVISOR

print(solve(row, column))
