import sys
from itertools import starmap

tape = {
    'children': lambda x: x == 3,
    'cats': lambda x: x > 7,
    'samoyeds': lambda x: x == 2,
    'pomeranians': lambda x: x < 3,
    'akitas': lambda x: x == 0,
    'vizslas': lambda x: x == 0,
    'goldfish': lambda x: x < 5,
    'trees': lambda x: x > 3,
    'cars': lambda x: x == 2,
    'perfumes': lambda x: x == 1,
}


def parse_aunt(line):
    aunt, things = line.split(':', 1)
    _name, number = aunt.split()
    amounts = {name.strip(): int(amount.strip())
               for name, amount in (thing.split(':')
                                    for thing in things.split(','))}
    return number, amounts

def matches(aunt):
    _number, things = aunt
    return all(starmap(lambda k, v: tape[k](v), things.items()))

aunts = map(parse_aunt, sys.stdin.readlines())
print(next(filter(matches, aunts))[0])