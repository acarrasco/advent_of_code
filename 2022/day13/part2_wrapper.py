import sys
import json
import functools
from itertools import zip_longest

def grouper(n, iterable, padvalue=None):
  "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
  return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

class IntWrapper(int):
    def __lt__(self, other):
        if isinstance(other, list):
            return [self] < other
        return super().__lt__(other)
    def __gt__(self, other):
        if isinstance(other, list):
            return [self] > other
        return super().__gt__(other)
    def __eq__(self, other):
        if isinstance(other, list):
            return [self] == other
        return super().__eq__(other)


def parse(lines):
    for left, right, _ in grouper(3, lines):
        yield json.loads(left, parse_int=IntWrapper)
        yield json.loads(right, parse_int=IntWrapper)
    yield [[IntWrapper(2)]]
    yield [[IntWrapper(6)]]


def solve(packets):
    ordered = sorted(packets)
    m = 1
    for n, packet in enumerate(ordered):
        if packet == [[2]] or packet == [[6]]:
            m *= n + 1
    return m

print(solve(parse(sys.stdin)))