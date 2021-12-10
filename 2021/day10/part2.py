import sys

opening_symbols = '({[<'
closing_symbols = ')}]>'
matching = dict(zip(opening_symbols, closing_symbols))

points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def stack_score(stack):
    total = 0
    for i in reversed(stack):
        total = total * 5 + points[i]
    print(stack, total)
    return total

def error_score(line):
    pending_stack = []
    for s in line:
        if s in opening_symbols:
            pending_stack.append(matching[s])
        else:
            if not pending_stack:
                return -1
            last_pending = pending_stack.pop()
            if last_pending != s:
                return -1
    if pending_stack:
        return stack_score(pending_stack)
    return -1

def positive(x):
    return x >= 0
error_scores = sorted(filter(positive, (error_score(line.strip()) for line in sys.stdin.readlines())))
print(error_scores[len(error_scores)//2])