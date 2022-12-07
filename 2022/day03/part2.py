import sys
import operator
from itertools import zip_longest
from functools import reduce

def priority(item):
    n = ord(item)
    if 65 <= n <= 90:
        return n - 38
    elif 97 <= n <= 122:
        return n - 96 
    else:
        raise ('Invalid item', item)

def find_repeated(ruckacks):
    return reduce(operator.and_, map(set, ruckacks))

def grouper(n, iterable, padvalue=None):
  "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
  return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

rucksacks = map(str.strip, sys.stdin.readlines())
groups = grouper(3, rucksacks)
repated_elements = list(map(find_repeated, groups))
priorities = [priority(*item) for item in repated_elements]
print(sum(priorities))