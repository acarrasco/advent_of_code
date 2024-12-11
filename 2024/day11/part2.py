import sys
import functools

def parse(line):
    return [int(c) for c in line.split()]

@functools.cache
def count_stones(stone, times):
    if times == 0:
        return 1
    if stone == 0:
        return count_stones(1, times - 1)
    digits = str(stone)
    l = len(digits)
    if l % 2 == 0:
        return count_stones(int(digits[:l//2]), times - 1) + count_stones(int(digits[l//2:]), times - 1)
    return count_stones(stone * 2024, times - 1)

def solve(stones, times=75):
    return sum(count_stones(stone, times) for stone in stones)

print(solve(parse(sys.stdin.read())))