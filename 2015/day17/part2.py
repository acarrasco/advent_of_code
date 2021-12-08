import sys
from collections import Counter


def combinations(containers, capacity, used):
    if capacity == 0:
        return Counter((used,))
    if capacity < 0 or not containers:
        return Counter()

    head, *tail = containers

    return (combinations(tail, capacity, used) +
            combinations(tail, capacity - head, used+1))


containers = sorted(map(int, sys.stdin.readlines()))

print(min(combinations(containers, 150, 0).items())[1])
