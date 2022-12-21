import sys

OPS = {
    '+': lambda x, y : x + y,
    '-': lambda x, y : x - y,
    '*': lambda x, y : x * y,
    '/': lambda x, y : x // y,
}

def parse(lines):
    monkeys = {}
    for line in lines:
        monkey, right = line.strip().split(':')
        monkeys[monkey] = right.split()
    return monkeys

def eval_monkey(monkeys, monkey):
    exp = monkeys[monkey]
    if len(exp) == 1:
        return int(exp[0])
    else:
        left, op, right = exp
        return OPS[op](eval_monkey(monkeys, left), eval_monkey(monkeys, right))

def solve(monkeys):
    return eval_monkey(monkeys, 'root')

print(solve(parse(sys.stdin)))