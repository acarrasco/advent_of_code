import sys

ROBOT = '@'
BOX = 'O'
EMPTY = '.'
WALL = '#'
LEFT_BOX = '['
RIGHT_BOX = ']'

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
                    robot = i, 2*j
                elif c == WALL:
                    result[i, 2*j] = WALL
                    result[i, 2*j+1] = WALL
                elif c == BOX:
                    result[i, 2*j] = LEFT_BOX
                    result[i, 2*j+1] = RIGHT_BOX

    return result, robot

def other_half(warehouse, position):
    i, j = position
    c = warehouse[position]
    if c == LEFT_BOX:
        return i, j+1
    elif c == RIGHT_BOX:
        return i, j-1

def parse(text):
    warehouse, movements = text.split('\n\n')
    return warehouse_to_dict(warehouse.split('\n')), ''.join(movements.replace('\n', ''))

def move(warehouse, robot, direction):
    i, j = robot
    di, dj = direction
    ni, nj = i + di, j + dj

    if (ni, nj) not in warehouse or try_push(warehouse, (ni, nj), direction):
        return warehouse, (ni, nj)
    else:
        return warehouse, robot

def try_push(warehouse, position, direction):
    if can_push(warehouse, position, direction):
        push(warehouse, position, direction)
        return True

def can_push(warehouse, position, direction, other=False):
    if warehouse.get(position) == WALL:
        return False

    i, j = position
    di, dj = direction
    ni, nj = i + di, j + dj

    empty_destination = (ni, nj) not in warehouse
    this_can_move = empty_destination or can_push(warehouse, (ni, nj), direction)

    other_moved = not di or other
    other_can_move = other_moved or can_push(warehouse, other_half(warehouse, position), direction, True)

    return this_can_move and other_can_move

def push(warehouse, position, direction, other=False):
    if warehouse.get(position) == WALL:
        raise Exception('pushing a wall')

    i, j = position
    di, dj = direction
    ni, nj = i + di, j + dj

    if (ni, nj) in warehouse:
        push(warehouse, (ni, nj), direction)

    need_move_other = di and not other
    if need_move_other:
        push(warehouse, other_half(warehouse, position), direction, True)

    warehouse[ni, nj] = warehouse[position]
    del warehouse[position]

def print_warehouse(warehouse, robot):
    rows, _ = max(warehouse)
    cols = max(c for _, c in warehouse)

    for i in range(rows+1):
        print(''.join((i, j) == robot and ROBOT or warehouse.get((i, j), EMPTY) for j in range(cols+1)))

def box_gps_positions(warehouse):
    total = 0
    for (i, j), c in warehouse.items():
        if c == LEFT_BOX:
            total += i * 100 + j
    return total

def solve(problem):
    (warehouse, robot), movements = problem
    for m in movements:
        # print(m)
        warehouse, robot = move(warehouse, robot, DIRECTIONS[m])
        # print_warehouse(warehouse, robot)
        # print()
    return box_gps_positions(warehouse)

print(solve(parse(sys.stdin.read())))