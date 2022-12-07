import sys
import itertools

def parse(line):
    if line.strip():
        return int(line)

def groups(items):
    return (g for k, g in itertools.groupby(items, lambda x: x is not None) if k)

print(max(map(sum, groups(map(parse, sys.stdin)))))