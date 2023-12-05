import sys
from collections import namedtuple, defaultdict

MappingRange = namedtuple("MappingRange", ["source_value", "target_value", "length"])
Mapping = namedtuple("Mapping", ["source", "target", "ranges"])
Problem = namedtuple("Problem", ["seeds", "mappings"])

def parse(lines):
    seeds = list(map(int,lines[0].split(":")[1].split()))
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


def convert_values(values, mapping_ranges):
    result = []
    for value in values:
        for mapping_range in mapping_ranges:
            if mapping_range.source_value <= value < mapping_range.source_value + mapping_range.length:
                result.append(mapping_range.target_value + value - mapping_range.source_value)
                break
        else:
            result.append(value)
    return result

def solve(problem):
    values = problem.seeds
    for mapping in problem.mappings:
        values = convert_values(values, mapping.ranges)
    return min(values)


def main():
    problem = parse(list(map(str.strip, sys.stdin.readlines())))
    solution = solve(problem)
    print(solution)

if __name__ == "__main__":
    main()