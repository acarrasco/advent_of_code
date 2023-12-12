import sys
from collections import namedtuple

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'
SENTINEL = '.'

def parse_line(line):
    layout, groups = line.strip().split(' ')
    expanded_layout = '?'.join([layout] * 5)
    expanded_groups = ','.join([groups] * 5)
    return expanded_layout + SENTINEL, tuple(int(group) for group in expanded_groups.split(','))

def first_different(layout, c):
    return next((i for i, x in enumerate(layout) if x != c), len(layout))

def memoize(f):
    cache = {}
    def memoized(*args, **kwargs):
        key = args
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return memoized

@memoize
def count_layouts(springs, damaged_group_sizes):
    expected_damaged = sum(damaged_group_sizes)
    if expected_damaged == 0:
        actual_damage = springs.count(DAMAGED)
        return int(actual_damage == 0)

    max_damaged = len(springs) - springs.count(OPERATIONAL)
    
    if expected_damaged > max_damaged:
        return 0
    
    if springs[0] == OPERATIONAL:
        next_non_operational = first_different(springs, OPERATIONAL)
        return count_layouts(springs[next_non_operational:], damaged_group_sizes)

    s = 0
    groups_head, *groups_tail = damaged_group_sizes
    can_match_group = springs[groups_head] != DAMAGED and OPERATIONAL not in springs[:groups_head]

    if can_match_group:
        s += count_layouts(springs[groups_head + 1:], tuple(groups_tail))
    if springs[0] == UNKNOWN:
        s += count_layouts(springs[1:], damaged_group_sizes)
    return s


print(sum(count_layouts(*parse_line(line)) for line in sys.stdin))