import sys

tape = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}


def parse_aunt(line):
    aunt, things = line.split(':', 1)
    _name, number = aunt.split()
    amounts = {name.strip(): int(amount.strip())
               for name, amount in (thing.split(':')
                                    for thing in things.split(','))}
    return number, amounts

def matches(aunt):
    number, things = aunt
    for thing in things:
        if tape[thing] != things[thing]:
            return False
    return True

aunts = map(parse_aunt, sys.stdin.readlines())
print(next(filter(matches, aunts))[0])