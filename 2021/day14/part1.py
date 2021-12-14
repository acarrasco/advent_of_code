import sys
import itertools
from collections import Counter


def not_empty(s):
    return s.strip()


def parse_line(line):
    return line.strip().split(' -> ')


def parse(lines):
    line_it = map(str.strip, lines)
    [source] = itertools.takewhile(not_empty, line_it)
    rules = dict(map(parse_line, line_it))
    return source, rules


def expand_once(rules, source):
    pairs = zip(source, source[1:])
    return ''.join(a + rules.get(a+b, '') for a, b in pairs) + source[-1]


def expand_times(rules, source, times):
    for _ in range(times):
        source = expand_once(rules, source)
    return source


def solve(rules, source, expansions):
    target = expand_times(rules, source, expansions)
    counts = Counter(target)
    hist = counts.most_common()
    return hist[0][1] - hist[-1][1]


input = sys.stdin
source, rules = parse(input)


print(solve(rules, source, 10))
