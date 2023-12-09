import sys
from pprint import pprint

def parse(lines):
    return [
        list(map(int, line.split())) for line in lines
    ]

def diffs(sequence):
    return [b - a for a, b in zip(sequence, sequence[1:])]

def extrapolate(sequence):
    # print(sequence)
    if all(x == 0 for x in sequence):
        return 0
    d = diffs(sequence)
    return sequence[-1] + extrapolate(d)

def solve(sequences):
    return sum(extrapolate(s) for s in sequences)

print(solve(parse(sys.stdin)))