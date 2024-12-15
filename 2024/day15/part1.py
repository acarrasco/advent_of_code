import sys

ROBOT = '@'
BOX = 'O'
EMPTY = '.'
WALL = '#'

DIRECTIONS = {
    '^': (-1, 0),
    'v': (1, 0),
    '>': (0, 1),
    '<': (0, -1),
}

def parse_line(line):
    return [int(x) for x in line.split()]

def warehouse_to_dict(warehouse):
    result = {}
    robot = None
    for i, row in enumerate(warehouse):
        for j, c in enumerate(row):
            if c != EMPTY:
                if c == ROBOT:
                    robot = i, j
                else:
                    result[i, j] = c
    return result, robot

def parse(text):
    warehouse, movements = text.split('\n\n')
    return warehouse_to_dict(warehouse.split('\n')), ''.join(movements.replace('\n', ''))

def move(warehouse, robot, direction):
    i, j = robot
    di, dj = direction
    ni, nj = i + di, j + dj

    if (ni, nj) not in warehouse or push(warehouse, (ni, nj), direction):
        return warehouse, (ni, nj)
    else:
        return warehouse, robot

def push(warehouse, position, direction):
    i, j = position
    di, dj = direction
    ni, nj = i + di, j + dj

    if warehouse.get(position) == WALL:
        return False

    if (ni, nj) not in warehouse or push(warehouse, (ni, nj), direction):
        warehouse[ni, nj] = warehouse[position]
        del warehouse[position]
        return True
    else:
        return False

def print_warehouse(warehouse, robot):
    rows, _ = max(warehouse)
    cols = max(c for _, c in warehouse)

    for i in range(rows+1):
        print(''.join((i, j) == robot and ROBOT or warehouse.get((i, j), EMPTY) for j in range(cols+1)))

def box_gps_positions(warehouse):
    total = 0
    for (i, j), c in warehouse.items():
        if c == BOX:
            total += i * 100 + j
    return total

def solve(problem):
    (warehouse, robot), movements = problem
    for m in movements:
        warehouse, robot = move(warehouse, robot, DIRECTIONS[m])
        # print_warehouse(warehouse, robot)
        # print()
        # print()
    return box_gps_positions(warehouse)

print(solve(parse(sys.stdin.read())))