import sys

def parse_elf(elf):
    a, b = elf.split('-')
    return int(a), int(b)

def parse(line):
    return tuple(map(parse_elf, line.strip().split(',')))

def overlaps(x):
    a, b = x
    a1, a2 = a
    b1, b2 = b

    return a2 >= b1 and a1 <= b2 or b2 >= a1 and b1 <= a2

print(sum(map(overlaps, map(parse, sys.stdin))))
