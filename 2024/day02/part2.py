import sys
import itertools

def parse(line):
    return map(int, line.split())

def solve(values):
    values = list(values)
    diffs = [x1 - x0 for x0, x1 in zip(values, values[1:])]
    signs = [d // abs(d) for d in diffs if d]
    sign = sum(signs)
    if sign:
        sign //= abs(sign)
    else:
        return False
    removed = False
    previous = values[0]
    for v in values[1:]:
        d = (v - previous) * sign
        if d > 3 or d <= 0:
            if removed:
                return all(0 < d * sign <= 3 for d in diffs[1:])
            removed = True
        else:
            previous = v
    return True

parsed_lines = map(parse, sys.stdin)
print(sum(map(solve, parsed_lines)))
