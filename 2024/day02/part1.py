import sys
import itertools

def parse(line):
    return map(int, line.split())

def solve(values):
    normal, delayed = itertools.tee(values)
    next(delayed)
    diffs = [x0 - x1 for x0, x1 in zip(normal, delayed)]
    if diffs[0]:
        sign = diffs[0] // abs(diffs[0])
    else:
        return 0
    return all(0 < d * sign <= 3 for d in diffs)

parsed_lines = map(parse, sys.stdin)
print(sum(map(solve, parsed_lines)))
