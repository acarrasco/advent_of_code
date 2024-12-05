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

def sort_sequence(ordering, s):
    ordered = list(s)
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            a = ordered[i]
            b = ordered[j]
            if (a, b) not in ordering:
                ordered[i], ordered[j] = ordered[j], ordered[i]
    return ordered

def solve(problem):
    ordering, updating_sequences = problem
    ordering = set(ordering)

    result = 0
    for unordered in updating_sequences:
        ordered = sort_sequence(ordering, unordered)
        if ordered != unordered:
            middle = ordered[len(ordered)//2]
            result += middle
    return result

print(solve(parse(sys.stdin)))