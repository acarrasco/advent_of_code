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
    def ways(pattern):
        if not pattern:
            return 1
        return sum(pattern.startswith(t) and ways(pattern[len(t):]) for t in towels)
    
    return sum(ways(p) for p in patterns)

print(solve(parse(sys.stdin)))
