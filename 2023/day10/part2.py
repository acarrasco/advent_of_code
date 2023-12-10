from collections import namedtuple
import sys
import os

LoopInfo = namedtuple('LoopInfo', ['loop', 'directions', 'left_turns', 'right_turns'])

DIRECTIONS = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}

NEIGHBORS = DIRECTIONS.values()

OPPOSITE_DIRECTIONS = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}

RIGHT = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'
}

LEFT = {b: a for a, b in RIGHT.items()}

SHAPE_DIRECTIONS = {
    '|': 'NS',
    '-': 'EW',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW',
    'F': 'SE',
    '.': '',
    'S': 'NESW',
}

DIRECTIONS_TO_PIPE = {
        'NE': '┌',
        'NW': '┐',
        'SE': '└',
        'SW': '┘',
        'EN': '┘',
        'ES': '┐',
        'WN': '└',
        'WS': '┌',
        'N': '│',
        'S': '│',
        'E': '─',
        'W': '─',
}

DIRECTIONS_TO_THICK_PIPE = {
        'NE': '╔',
        'NW': '╗',
        'SE': '╚',
        'SW': '╝',
        'EN': '╝',
        'ES': '╗',
        'WN': '╚',
        'WS': '╔',
        'N': '║',
        'S': '║',
        'E': '═',
        'W': '═',
}

DIRECTIONS_TO_ARROW = {
        'NE': '↱',
        'NW': '↰',
        'SE': '↳',
        'SW': '↲',
        'EN': '⬏',
        'ES': '⬎',
        'WN': '⬑',
        'WS': '⬐',
        'N': '↑',
        'S': '↓',
        'E': '→',
        'W': '←',
}

def pretty_print(problem, loop_info, area,
                 direction_to_glyph=DIRECTIONS_TO_THICK_PIPE,
                 start_char='❊',
                 fill_char='░',
                 empty_char='·'):
    glyphs = {}
    positions, directions, _, _ = loop_info
    for p, d in zip(positions, directions):
        glyphs[p] = direction_to_glyph[d]

    for i, line in enumerate(problem):
        print(''.join(c == 'S' and start_char or
                      glyphs.get((i,j)) or 
                      (i,j) in area and fill_char or empty_char
                       for j, c in enumerate(line)))

def parse(lines):
    return [line.strip() for line in lines]

def find_start(problem):
    for i, row in enumerate(problem):
        for j, cell in enumerate(row):
            if cell == 'S':
                return (i, j)
    raise "No start found"

def connected_shapes(from_shape, direction, to_shape):
    can_move_from = direction in SHAPE_DIRECTIONS[from_shape]
    can_arrive_to = OPPOSITE_DIRECTIONS[direction] in SHAPE_DIRECTIONS[to_shape]
    return can_move_from and can_arrive_to

def get_next_direction(direction, to_shape):
    if to_shape == 'S':
        return ''
    arrive_from_direction = OPPOSITE_DIRECTIONS[direction]
    return SHAPE_DIRECTIONS[to_shape].replace(arrive_from_direction, '')

def move(problem, position, direction):
    i, j = position
    di, dj = DIRECTIONS[direction]
    if 0 <= i + di < len(problem) and 0 <= j + dj < len(problem[0]):
        from_shape = problem[i][j]
        to_shape = problem[i + di][j + dj]
        if connected_shapes(from_shape, direction, to_shape):
            return (i + di, j + dj), get_next_direction(direction, to_shape)
    return None, None

def find_loop(problem, start, direction) -> LoopInfo:
    position = start
    steps = []
    directions = []
    right_turns = 0
    left_turns = 0
    while True:
        position, next_direction = move(problem, position, direction)
        if position is None:
            return
        
        if next_direction == direction:
            directions.append(direction)
        else:
            directions.append(direction + next_direction)
            if RIGHT[direction] == next_direction:
                right_turns += 1
            elif LEFT[direction] == next_direction:
                left_turns += 1
        
        direction = next_direction
        steps.append(position)

        if position == start:
            return LoopInfo(steps, directions, left_turns, right_turns)


def area_enclosed_by_loop(loop_info):
    loop, directions, left_turns, right_turns = loop_info
    bounds = set(loop)

    if left_turns > right_turns:
        inside_normal = LEFT
    else:
        inside_normal = RIGHT
    
    area = set()
    for (i, j), direction in zip(loop, directions):
        for d in direction:
            normal_di, normal_dj = DIRECTIONS[inside_normal[d]]
            update_inside_area(bounds, (i + normal_di, j + normal_dj), area)
    return area

def update_inside_area(bounds, inside_point, visited):
    if inside_point in bounds or inside_point in visited:
        return
    backtracking_stack = [inside_point]
    visited.add(inside_point)
    while backtracking_stack:
        i, j = backtracking_stack.pop()
        for di, dj in NEIGHBORS:
            candidate = i + di, j + dj
            if candidate not in bounds and candidate not in visited:
                visited.add(candidate)
                backtracking_stack.append(candidate)

def solve(problem):
    start = find_start(problem)
    loop_info = next(filter(None, (find_loop(problem, start, direction) for direction in DIRECTIONS)))
    area = area_enclosed_by_loop(loop_info)
    pretty_print(problem, loop_info, area)
    return area

def test_case(filename, expected):
    local = os.path.dirname(__file__)
    problem = parse(open(os.path.join(local, filename)))
    result = solve(problem)
    if len(result) != expected:
        print(f'{filename}: expected {expected}, got {len(result)}')
    print()

test_case('test00.txt', 0)
test_case('test01.txt', 1)
test_case('test02.txt', 1)
test_case('test03.txt', 4)
test_case('test04.txt', 4)
test_case('test05.txt', 8)
test_case('test06.txt', 10)
test_case('test07.txt', 9)
test_case('test08.txt', 4)
test_case('test09.txt', 4)
test_case('test10.txt', 4)
test_case('test11.txt', 1)

print(len(solve(parse(sys.stdin))))