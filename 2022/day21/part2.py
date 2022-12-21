import sys

OPS = {
    '+': lambda x, y : x + y if x is not None and y is not None else None,
    '-': lambda x, y : x - y if x is not None and y is not None else None,
    '*': lambda x, y : x * y if x is not None and y is not None else None,
    '/': lambda x, y : x // y if x is not None and y is not None else None,
}

SOLVE_R = {
    '+': lambda res, left : res - left,
    '-': lambda res, left : left - res,
    '*': lambda res, left : res // left,
    '/': lambda res, left : left // res,
}

SOLVE_L = {
    '+': lambda res, right : res - right,
    '-': lambda res, right : res + right,
    '*': lambda res, right : res // right,
    '/': lambda res, right : res * right,
}

def parse(lines):
    monkeys = {}
    for line in lines:
        monkey, right = line.strip().split(':')
        monkeys[monkey] = right.strip().split()
    left, _, right = monkeys['root']

    del monkeys['humn']
    del monkeys['root']
    return monkeys, left, right, 'humn'

def eval_monkey(monkeys, monkey, cached):
    if monkey not in monkeys:
        return None
    exp = monkeys[monkey]
    if len(exp) == 1:
        cached[monkey] = int(exp[0])
    elif monkey not in cached:
        left, op, right = exp
        res = OPS[op](eval_monkey(monkeys, left, cached), eval_monkey(monkeys, right, cached))
        cached[monkey] = res
    return cached[monkey]

def solve_unknown(monkeys, unknown, known_value, monkey, cached):
    if monkey == unknown:
        return known_value

    left, op, right = monkeys[monkey]
    left_value = eval_monkey(monkeys, left, cached)
    right_value = eval_monkey(monkeys, right, cached)
    if left_value is not None:
        next_known_value = SOLVE_R[op](known_value, left_value)
        return solve_unknown(monkeys, unknown, next_known_value, right, cached)
    if right_value is not None:
        next_known_value = SOLVE_L[op](known_value, right_value)
        return solve_unknown(monkeys, unknown, next_known_value, left, cached)
    
    raise Exception('Cannot eval %s: %s %s %s' % (monkey, left, op, right))

def solve(monkeys, left, right, unknown):
    cached = {}
    eval_left = eval_monkey(monkeys, left, cached)
    eval_right = eval_monkey(monkeys, right, cached)
    unknown_branch = eval_left is None and left or right
    known_branch_value = eval_left is None and eval_right or eval_left
    return solve_unknown(monkeys, unknown, known_branch_value, unknown_branch, cached)

print(solve(*parse(sys.stdin)))