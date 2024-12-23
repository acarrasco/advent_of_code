import sys
from collections import defaultdict
import itertools

def parse(lines):
    return set(line.strip() for line in lines)

def count_candidate_triplets(links):
    connections = defaultdict(set)
    chains = set()

    for link in links:
        a, b = link.split('-')
        connections[a].add(b)
        connections[b].add(a)

    def count_chains(node, chain, depth):
        if depth == 0:
            yield chain
            return
        for c in connections[node]:
            if c not in chain:
                yield from count_chains(c, chain + (c,), depth - 1)

    for a, aconns in connections.items():
        if a[0] == 't':
            for b, c in itertools.combinations(aconns, 2):
                if f'{b}-{c}' in links or f'{c}-{b}' in links:
                    chains.add(','.join(sorted([a, b, c])))

    for c in sorted(chains):
        print(c)

    return len(chains)

def solve(problem):
    return count_candidate_triplets(problem)

print(solve(parse(sys.stdin)))
