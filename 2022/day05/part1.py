import sys
from itertools import zip_longest
from collections import defaultdict

lines = sys.stdin.readlines()

def grouper(n, iterable, padvalue=None):
  "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
  return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def parse_stacks(lines):
    stacks = defaultdict(list)
    for line in lines:
        for n, item in enumerate(grouper(4, line, ' ')):
            if item[1] != ' ':
                stacks[str(n + 1)].append(item[1])
    return {k: stacks[k][::-1] for k in sorted(stacks, key=int)}

def parse_commands(lines):
    for line in lines:
        _, n, _, a, _, b = line.split()
        yield int(n), a, b

def parse(lines):
    separator = lines.index('\n')
    return parse_stacks(lines[:separator-1]), parse_commands(lines[separator+1:])

def solve(stacks, commands):
    for n, a, b in commands:
        for _ in range(n):
            stacks[b].append(stacks[a].pop())
    return ''.join(stacks[s][-1] for s in sorted(stacks, key=int))
        

print(solve(*parse(lines)))