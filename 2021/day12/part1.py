import sys
from collections import defaultdict


def explore(graph, end, visited, current):
    if current.islower() and current in visited:
        return 0

    visited_plus_current = visited | {current}
    if current == end and len(visited_plus_current) == len(graph):
        return 1

    all_branches = (explore(graph, end, visited_plus_current, next_node)
                    for next_node in graph.get(current))
    return sum(all_branches)


def solve(graph, start, end):
    return explore(graph, end, set(), start)


def build_graph(lines):
    g = defaultdict(list)
    for line in lines:
        a, b = line.strip().split('-')
        if a != 'start' and b != 'end':
            g[b].append(a)
        if b != 'start' and a != 'end':
            g[a].append(b)
    return g


input = sys.stdin


graph = build_graph(input)
print(solve(graph, 'start', 'end'))
