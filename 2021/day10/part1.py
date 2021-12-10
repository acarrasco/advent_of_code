import sys

opening_symbols = '({[<'
closing_symbols = ')}]>'
matching = dict(zip(opening_symbols, closing_symbols))

points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def error_score(line):
    pending_stack = []
    for s in line:
        if s in opening_symbols:
            pending_stack.append(matching[s])
        else:
            if not pending_stack:
                print('empty stack', line, s)
                return points[s]
            last_pending = pending_stack.pop()
            if last_pending != s:
                print('not matching', line, s, last_pending)
                return points[s]
    return 0

print(sum(error_score(line.strip()) for line in sys.stdin.readlines()))