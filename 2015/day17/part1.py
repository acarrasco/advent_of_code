import sys


containers = sorted(map(int, sys.stdin.readlines()))


def combinations(containers, capacity):
    if capacity == 0:
        return 1
    if capacity < 0 or not containers:
        return 0

    head, *tail = containers
    return combinations(tail, capacity) + combinations(tail, capacity - head)

print(combinations(containers, 150))