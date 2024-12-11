import sys
import itertools

def parse(line):
    return [int(c) for c in line.split()]

def change(stone):
    if stone == 0:
        return [1]
    digits = str(stone)
    l = len(digits)
    if l % 2 == 0:
        return [int(digits[:l//2]), int(digits[l//2:])]
    return [stone * 2024]

def solve(stones, times=25):
    for _ in range(times):
        stones = itertools.chain(*map(change, stones))
    return sum(1 for _ in stones)

print(solve(parse(sys.stdin.read())))