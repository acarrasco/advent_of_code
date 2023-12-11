import sys


def parse_input(lines):
    return [list(line.strip()) for line in lines]


def find_galaxies(lines):
    galaxies = []
    rows_with_galaxies = set()
    columns_with_galaxies = set()

    for i, row in enumerate(lines):
        for j, col in enumerate(row):
            if col == '#':
                galaxies.append((i, j))
                rows_with_galaxies.add(i)
                columns_with_galaxies.add(j)

    return galaxies

def expand_empty_rows(universe):
    new_universe = []
    for row in universe:
        if '#' in row:
            new_universe.append(row)
        else:
            new_universe.append(['.'] * len(row))
            new_universe.append(['.'] * len(row))
    return new_universe

def expand_universe(universe):
    expanded_rows = expand_empty_rows(universe)
    expanded_columns = expand_empty_rows(list(zip(*expanded_rows)))
    return list(zip(*expanded_columns))

def calculate_distances(universe):

    galaxies = find_galaxies(universe)
    
    total = 0
    for i, a in enumerate(galaxies):
        for j, b in enumerate(galaxies):
            if j > i:
                d = abs(a[0] - b[0]) + abs(a[1] - b[1])
                total += d
    
    return total

universe = parse_input(sys.stdin.readlines())
expanded_universe = expand_universe(universe)

print(calculate_distances(expanded_universe))