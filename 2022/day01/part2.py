import sys
import itertools
import heapq

def parse(line):
    if line.strip():
        return int(line)

def groups(items):
    return (g for k, g in itertools.groupby(items, lambda x: x is not None) if k)

print(sum(heapq.nlargest(3, (map(sum, groups(map(parse, sys.stdin)))))))