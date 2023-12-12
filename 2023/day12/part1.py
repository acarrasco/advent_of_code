import sys
from collections import namedtuple
from itertools import groupby, product

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'
DamageRecord = namedtuple('DamageRecord', ['layout', 'contiguous_damaged_group_sizes'])

def parse_line(line):
    layout, groups = line.strip().split(' ')
    return DamageRecord(layout, [int(group) for group in groups.split(',')])

def fits_arrangement(layout, expected_damaged_group_sizes):
    expected_damaged_group_sizes = [x for x in expected_damaged_group_sizes if x > 0]
    actual_damaged_group_sizes = [len(list(group_size)) for c, group_size in groupby(layout) if c == DAMAGED]
    return actual_damaged_group_sizes == expected_damaged_group_sizes

def replace_unknowns(layout, replacement):
    it = iter(replacement)
    return ''.join(c if c != UNKNOWN else next(it) for c in layout)

def count_how_many_possible_layouts(damage_record):
    layout, damaged_group_sizes = damage_record
    unknowns = layout.count(UNKNOWN)
    if unknowns == 0:
        all_possible_layouts = [layout]
    else:
        replacements = product([OPERATIONAL, DAMAGED], repeat=unknowns)
        all_possible_layouts = (replace_unknowns(layout, replacement) for replacement in replacements)
    return sum(fits_arrangement(layout, damaged_group_sizes) for layout in all_possible_layouts)

print(sum(count_how_many_possible_layouts(parse_line(line)) for line in sys.stdin.readlines()))