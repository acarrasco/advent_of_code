import sys

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

def calculate_directions(cell, direction):
    if cell == '/':
        if direction == NORTH: return [EAST]
        if direction == EAST: return [NORTH]
        if direction == SOUTH: return [WEST]
        if direction == WEST: return [SOUTH]
    elif cell == '\\':        
        if direction == NORTH: return [WEST]
        if direction == EAST: return [SOUTH]
        if direction == SOUTH: return [EAST]
        if direction == WEST: return [NORTH]
    elif cell == '|':
        if direction == NORTH: return [NORTH]
        if direction == EAST: return [NORTH, SOUTH]
        if direction == SOUTH: return [SOUTH]
        if direction == WEST: return [NORTH, SOUTH]
    elif cell == '-':
        if direction == NORTH: return [EAST, WEST]
        if direction == EAST: return [EAST]
        if direction == SOUTH: return [EAST, WEST]
        if direction == WEST: return [WEST]
    elif cell == '.': return [direction]

DIRECTION_SYMBOLS = {
    NORTH: '^',
    EAST: '>',
    SOUTH: 'v',
    WEST: '<',
}

def print_visited(visited, rows, cols):
    m = [['.' for _ in range(cols)] for _ in range(rows)]
    for d, i,j in visited:
        if m[i][j] == '.':
            m[i][j] = DIRECTION_SYMBOLS[d]
        elif m[i][j] in DIRECTION_SYMBOLS.values():
            m[i][j] = '2'
        else:
            m[i][j] = str(int(m[i][j]) + 1)
    for row in m:
        print(''.join(row))
    print()

def simulate(problem, initial_beam):
    rows = len(problem)
    cols = len(problem[0])
    beams_heads = [initial_beam]
    visited = set()

    while beams_heads:
        next_beams = []
        for (di, dj), i, j in beams_heads:
            ni, nj = i + di, j + dj
            beam = ((di, dj), ni, nj)
            if 0 <= ni < rows and 0 <= nj < cols and beam not in visited:
                visited.add(beam)
                cell = problem[ni][nj]
                next_directions = calculate_directions(cell, (di, dj))
                for next_direction in next_directions:
                    next_beams.append((next_direction, ni, nj))
        beams_heads = next_beams
    return visited

def calculate_energized(visited):
    energized = set()
    for _, i, j in visited:
        energized.add((i, j))
    return energized

def parse_line(line):
    return line.strip()

def parse(lines):
    return [parse_line(line) for line in lines]

def solve_one(problem, initial_beam):
    visited = simulate(problem, initial_beam)
    energized = calculate_energized(visited)
    return len(energized)

def find_all_solutions(problem):
    rows = len(problem)
    columns = len(problem[0])
    for row in range(rows):
        yield solve_one(problem, (EAST, row, -1))
        yield solve_one(problem, (WEST, row, columns))
    for col in range(columns):
        yield solve_one(problem, (SOUTH, -1, col))
        yield solve_one(problem, (NORTH, rows, col))

def solve(problem):
    return max(find_all_solutions(problem))

input = sys.stdin.readlines()
print(solve(parse(input)))