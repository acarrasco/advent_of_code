import sys

def parse(lines):
    ordering = []
    updating_sequences = []

    lines_it = iter(lines)
    line = next(lines_it).strip()
    while line:
        ordering.append(tuple(int(x) for x in line.split('|')))
        line = next(lines_it, '').strip()
    line = next(lines_it, '').strip()
    while line:
        updating_sequences.append([int(x) for x in line.split(',')])
        line = next(lines_it, '').strip()
    return ordering, updating_sequences

def solve(problem):
    ordering, updating_sequences = problem
    ordering = set(ordering)

    result = 0
    for s in updating_sequences:
        if all(x in ordering for x in zip(s, s[1:])):
            middle = s[len(s)//2]
            result += middle
    return result

print(solve(parse(sys.stdin)))