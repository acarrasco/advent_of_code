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

    return galaxies, rows_with_galaxies, columns_with_galaxies


def calculate_distance(a, b, rows_with_galaxies, columns_with_galaxies, expansion_factor):
    total = 0
    min_row = min(a[0], b[0])
    max_row = max(a[0], b[0])
    for row in range(min_row, max_row):
        if row in rows_with_galaxies:
            total += 1
        else:
            total += expansion_factor

    min_col = min(a[1], b[1])
    max_col = max(a[1], b[1])
    for col in range(min_col, max_col):
        if col in columns_with_galaxies:
            total += 1
        else:
            total += expansion_factor
    return total

def calculate_distances(universe, expansion_factor=1000000):

    galaxies, rows_with_galaxies, columns_with_galaxies = find_galaxies(universe)
    
    total = 0
    for i, a in enumerate(galaxies):
        for j, b in enumerate(galaxies):
            if j > i:
                d = calculate_distance(a, b, rows_with_galaxies, columns_with_galaxies, expansion_factor)
                total += d
    return total

universe = parse_input(sys.stdin.readlines())

print(calculate_distances(universe))