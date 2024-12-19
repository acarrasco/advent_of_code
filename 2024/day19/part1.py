import sys
import functools

def parse_line(line):
    return [x.strip() for x in line.split(',')]

def parse(lines):
    lines_iter = iter(lines)
    towels = parse_line(next(lines_iter))
    next(lines_iter)
    patterns = [line.strip() for line in lines_iter]
    return towels, patterns

def solve(problem):
    towels, patterns = problem

    @functools.cache
    def can_match(pattern):
        if not pattern:
            return True
        for towel in towels:
            if pattern.startswith(towel) and can_match(pattern[len(towel):]):
                return True
        return False

    return sum(can_match(p) for p in patterns)

print(solve(parse(sys.stdin)))
