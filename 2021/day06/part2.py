import sys
from collections import Counter


def cycle(fish_counts, max_days=8):
    result = {}

    for i in range(1, max_days + 1):
        result[i - 1] = fish_counts.get(i, 0)
    result[8] = fish_counts.get(0, 0)
    result[6] = result.get(6, 0) + fish_counts.get(0, 0)
    return result


def simulate(fish_counts, days):
    for _ in range(days):
        fish_counts = cycle(fish_counts)
    return sum(fish_counts.values())


fish_counts = Counter(map(int, sys.stdin.read().strip().split(',')))

print(simulate(fish_counts, 256))
