import sys
import itertools
from collections import Counter, defaultdict


def not_empty(s):
    return s.strip()


def parse_line(line):
    return line.strip().split(' -> ')


def parse(lines):
    line_it = map(str.strip, lines)
    [source] = itertools.takewhile(not_empty, line_it)
    rules = dict(map(parse_line, line_it))
    return source, rules


def expand_once(rules, pairs_counts):
    res = defaultdict(int)
    for (a, c), times in pairs_counts.items():
        b = rules.get(a+c)
        if b:
            res[a + b] += times
            res[b + c] += times
        else:
            res[a+c] += times

    return res


def expand_times(rules, source, times):
    pairs_counts = Counter(zip(source, source[1:]))
    for _ in range(times):
        pairs_counts = expand_once(rules, pairs_counts)
    return pairs_counts


def unwrap_pairs(pair_counts):
    counts = defaultdict(int)
    for (a, b), count in pair_counts.items():
        counts[a] += count
        counts[b] += count
    return counts


def solve(rules, source, expansions):
    target = expand_times(rules, source, expansions)
    left_edge = source[0]
    right_edge = source[-1]

    double_counted = unwrap_pairs(target)    
    double_counted[left_edge] += 1
    double_counted[right_edge] += 1

    most_repeated = max(double_counted.items(), key=lambda kv: kv[1])[1] // 2
    least_repeated = min(double_counted.items(), key=lambda kv: kv[1])[1] // 2
    
    return most_repeated - least_repeated


input = sys.stdin
source, rules = parse(input)
print(solve(rules, source, 40))
