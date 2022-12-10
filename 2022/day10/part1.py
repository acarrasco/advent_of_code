import sys

SAMPLE_CYCLES = set((20, 60, 100, 140, 180, 220))

def parse(line):
    tokens = line.strip().split()
    if len(tokens) == 1:
        return 1, 0
    else:
        return 2, int(tokens[1])

def solve(instructions):
    cycle = 0
    signal = 0
    x = 1
    for delay, value in instructions:
        for _ in range(delay):
            cycle += 1
            if cycle in SAMPLE_CYCLES:
                signal += cycle * x
        x += value
    return signal
        

print(solve(map(parse, sys.stdin)))