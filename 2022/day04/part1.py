import sys

def parse_elf(elf):
    a, b = elf.split('-')
    return int(a), int(b)

def parse(line):
    return tuple(map(parse_elf, line.strip().split(',')))

def contains(x):
    a, b = x
    a1, a2 = a
    b1, b2 = b

    return a1 <= b1 and a2 >= b2 or b1 <= a1 and b2 >= a2


print(sum(map(contains, map(parse, sys.stdin))))
