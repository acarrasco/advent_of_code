import sys
from collections import namedtuple
from pprint import pprint

MappingRange = namedtuple("MappingRange", ["source_value", "target_value", "length"])
ValueRange = namedtuple("ValueRange", ["value", "length"])
Mapping = namedtuple("Mapping", ["source", "target", "ranges"])
Problem = namedtuple("Problem", ["seeds", "mappings"])

def parse(lines):
    seeds_tokens = list(map(int,lines[0].split(":")[1].split()))
    seeds = []
    for i in range(0, len(seeds_tokens), 2):
        seeds.append(ValueRange(seeds_tokens[i], seeds_tokens[i+1]))

    mappings = []

    for line in lines[1:]:
        if line.endswith("map:"):
            source, target = line.split()[0].split("-to-")
            current_mapping_ranges = []
            mappings.append(Mapping(source, target, current_mapping_ranges))
        elif line:
            tokens = line.split()
            current_mapping_ranges.append(MappingRange(int(tokens[1]), int(tokens[0]), int(tokens[2])))

    return Problem(seeds, mappings)

def range_intersection(range1, range2):
    """
    Returns the intersection of range1 and range2, or None if they don't intersect.
    
    >>> range_intersection(ValueRange(0, 10), ValueRange(5, 10))
    ValueRange(value=5, length=5)

    >>> range_intersection(ValueRange(0, 10), ValueRange(10, 10))

    >>> range_intersection(ValueRange(5, 10), ValueRange(0, 3))

    >>> range_intersection(ValueRange(0, 10), ValueRange(7, 10))
    ValueRange(value=7, length=3)
    """
    if range1.value > range2.value:
        range1, range2 = range2, range1
    if range1.value + range1.length <= range2.value:
        return None
    return ValueRange(range2.value, min(range1.value + range1.length, range2.value + range2.length) - range2.value)

def range_subtract(range1, ranges):
    """
    Returns the parts of range1 that are not by ranges.

    >>> range_subtract(ValueRange(0, 10), [ValueRange(0, 5)])
    [ValueRange(value=5, length=5)]

    >>> range_subtract(ValueRange(0, 10), [ValueRange(1, 2), ValueRange(5, 3)])
    [ValueRange(value=0, length=1), ValueRange(value=3, length=2), ValueRange(value=8, length=2)]
    """
    result = []
    for range2 in sorted(ranges):
        intersection = range_intersection(range1, range2)
        if intersection:
            left = ValueRange(range1.value, intersection.value - range1.value)
            if left.length > 0:
                result.append(left)
            right = ValueRange(intersection.value + intersection.length, range1.length - intersection.length - left.length)
            range1 = right
    if range1.length > 0:
        result.append(range1)
    return result


def convert_values(value_ranges, mapping_ranges):
    result = []
    for seed_start, seed_length in value_ranges:
        current_range_intersections = []
        seed_range = ValueRange(seed_start, seed_length)
        for source_value, target_value, mapping_length in mapping_ranges:
            source_range = ValueRange(source_value, mapping_length)
            seed_source_intersect = range_intersection(seed_range, source_range)
            if seed_source_intersect:
                result.append(ValueRange(target_value + seed_source_intersect.value - source_value, seed_source_intersect.length))
                current_range_intersections.append(seed_source_intersect)
        result.extend(range_subtract(seed_range, current_range_intersections))

    return result

def solve(problem):
    value_ranges = problem.seeds
    for mapping in problem.mappings:
        value_ranges = convert_values(value_ranges, mapping.ranges)
    return min(value_ranges).value


def main():
    problem = parse(list(map(str.strip, sys.stdin.readlines())))
    solution = solve(problem)
    print(solution)

if __name__ == "__main__":
    main()