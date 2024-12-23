import sys
from collections import defaultdict

def parse(lines):
    return set(line.strip() for line in lines)

def get_groups(links):
    connections = defaultdict(set)

    groups = set()
    for link in links:
        a, b = link.split('-')
        connections[a].add(b)
        connections[b].add(a)
        groups.add(','.join(sorted({a, b})))

    while len(groups) > 1:
        next_groups = set()
        for g in groups:
            g = set(g.split(','))
            for c in connections:
                if c not in g and g.issubset(connections[c]):
                    g.add(c)
                    next_groups.add(','.join(sorted(g)))
                    break
        groups = next_groups
    result, = groups
    return result

def solve(problem):
    return get_groups(problem)

print(solve(parse(sys.stdin)))
