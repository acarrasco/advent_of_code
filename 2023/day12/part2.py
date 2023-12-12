import sys
from collections import namedtuple

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'

def parse_line(line):
    layout, groups = line.strip().split(' ')
    expanded_layout = '?'.join([layout] * 5)
    expanded_groups = ','.join([groups] * 5)
    return expanded_layout, tuple(int(group) for group in expanded_groups.split(',')), False

def memoize(f):
    cache = {}
    def memoized(*args, **kwargs):
        key = args
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return memoized

@memoize
def count_layouts(springs, damaged_group_sizes, running_group):
    expected_damaged = sum(damaged_group_sizes)
    if expected_damaged == 0:
        if springs.count(DAMAGED) == 0:
            return 1
        else:
            return 0
    operating = springs.count(OPERATIONAL)
    max_damaged = len(springs) - operating

    if expected_damaged > max_damaged:
        return 0

    if not springs:
        return int(sum(damaged_group_sizes) == 0)
    
    springs_head, springs_tail = springs[0], springs[1:]
    groups_head, *groups_tail = damaged_group_sizes
    groups_tail = tuple(groups_tail)

    if springs_head == OPERATIONAL:
        if groups_head == 0:
            return count_layouts(springs_tail, groups_tail, False)
        elif running_group:
            return 0
        else:
            return count_layouts(springs_tail, damaged_group_sizes, False)
    elif springs_head == DAMAGED:
        if groups_head == 0:
            return 0
        else:
            return count_layouts(springs_tail, (groups_head - 1,) + groups_tail, True)
    elif springs_head == UNKNOWN and groups_head == 0:
        return count_layouts(springs_tail, groups_tail, False)
    elif running_group:
        return count_layouts(springs_tail, (groups_head - 1,) + groups_tail, True)
    
    return (count_layouts(DAMAGED + springs_tail, damaged_group_sizes, False) + 
            count_layouts(springs_tail, damaged_group_sizes, False))


print(sum(count_layouts(*parse_line(line)) for line in sys.stdin))