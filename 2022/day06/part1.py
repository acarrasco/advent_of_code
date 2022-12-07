import sys

MARKER_SIZE = 4

def solve(input):
    for i in range(MARKER_SIZE, len(input)):
        if len(set(input[i-MARKER_SIZE:i])) == MARKER_SIZE:
            return i

print(solve(sys.stdin.read().strip()))