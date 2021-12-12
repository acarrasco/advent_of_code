import sys
import itertools
import re
from collections import defaultdict

element_exp = '[eA-Z][a-z]?'
inf = float('inf')


def parse_transmutation(line):
    left, *right = re.findall(element_exp, line)
    return left, ''.join(right)


def not_empty(s):
    return s.strip()


def parse(lines):
    line_it = map(str.strip, lines)
    transmutation_lines = list(itertools.takewhile(not_empty, line_it))
    reduction_rules = {}
    for line in transmutation_lines:
        left, right = parse_transmutation(line)
        reduction_rules[right] = left
    target_molecule = next(line_it)
    return reduction_rules, target_molecule


def a_star(start, goal, neighbors, h):
    open_set = {start}

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)

    while open_set:
        current = min(open_set, key=f_score.__getitem__)
        if current == goal:
            return g_score[current]

        open_set.remove(current)
        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                fs = tentative_g_score + h(neighbor)
                if fs != inf:
                    f_score[neighbor] = fs
                open_set.add(neighbor)
    return None


def top_down_reductions(reduction_rules, molecule):
    for src, dst in reduction_rules.items():
        for m in re.finditer(src, molecule):
            yield molecule[:m.start()] + dst + molecule[m.end():]


reduction_rules, target = parse(sys.stdin.readlines())


def neighbors(node): return top_down_reductions(reduction_rules, node)


print(a_star(target, 'e', neighbors, h=len))
