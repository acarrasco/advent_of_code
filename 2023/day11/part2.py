import sys


def parse_input(lines):
    return [list(line.strip()) for line in lines]

def calculate_offsets(size, expansion_factor, occupied):
    offsets = []
    expanded = 0
    for i in range(size):
        offsets.append(expanded)
        if i in occupied:
            expanded += 1
        else:
            expanded += expansion_factor
    return offsets

def calculate_row_and_column_offsets(rows, columns, rows_with_galaxies, columns_with_galaxies, expansion_factor):
    row_offsets = calculate_offsets(rows, expansion_factor, rows_with_galaxies)
    column_offsets = calculate_offsets(columns, expansion_factor, columns_with_galaxies)
    return row_offsets, column_offsets

def find_galaxies_and_offsets(lines, expansion_factor):
    galaxies = []
    rows_with_galaxies = set()
    columns_with_galaxies = set()

    for i, row in enumerate(lines):
        for j, col in enumerate(row):
            if col == '#':
                galaxies.append((i, j))
                rows_with_galaxies.add(i)
                columns_with_galaxies.add(j)

    rows = len(lines)
    cols = len(lines[0])
    return galaxies, calculate_row_and_column_offsets(rows, cols, rows_with_galaxies, columns_with_galaxies, expansion_factor)


def calculate_distances(universe, expansion_factor=1000000):
    galaxies, (row_offsets, column_offsets) = find_galaxies_and_offsets(universe, expansion_factor)
    
    total = 0
    for ga, (gai, gaj) in enumerate(galaxies):
        for gb, (gbi, gbj) in enumerate(galaxies):
            if gb > ga:
                real_ai, real_aj = row_offsets[gai], column_offsets[gaj]
                real_bi, real_bj = row_offsets[gbi], column_offsets[gbj]
                d = abs(real_ai - real_bi) + abs(real_aj - real_bj)
                total += d
    return total

universe = parse_input(sys.stdin.readlines())

print(calculate_distances(universe))