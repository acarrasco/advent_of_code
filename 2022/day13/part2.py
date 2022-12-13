import sys
import json
import functools
from itertools import zip_longest

def grouper(n, iterable, padvalue=None):
  "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
  return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    if left and right:
        left_head, *left_tail = left
        right_head, *right_tail = right
        return compare(left_head, right_head) or compare(left_tail, right_tail)

    return len(left) - len(right)

def parse(lines):
    for left, right, _ in grouper(3, lines):
        yield json.loads(left)
        yield json.loads(right)
    yield [[2]]
    yield [[6]]


def solve(packets):
    ordered = sorted(packets, key=functools.cmp_to_key(compare))
    m = 1
    for n, packet in enumerate(ordered):
        if packet == [[2]] or packet == [[6]]:
            m *= n + 1
    return m

print(solve(parse(sys.stdin)))