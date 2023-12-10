import sys

DIRECTIONS = {
    'N': ( -1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}

OPPOSITE_DIRECTIONS = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}

PIPE_SHAPES = {
    '|': 'NS',
    '-': 'EW',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW',
    'F': 'SE',    
}

def parse(lines):
    return [
        list(line.strip('\n')) for line in lines
    ]

def find_start(problem):
    for i, row in enumerate(problem):
        for j, cell in enumerate(row):
            if cell == 'S':
                return (i, j)

def neighbors(problem, position):
    i, j = position
    for direction, (di, dj) in DIRECTIONS.items():
        if 0 <= i + di < len(problem) and 0 <= j + dj < len(problem[0]):
            yield (i + di, j + dj)

def compatible_shapes(from_shape, direction, to_shape):
    can_move_from = from_shape == 'S' or direction in PIPE_SHAPES[from_shape]
    can_arrive_to = to_shape == 'S' or OPPOSITE_DIRECTIONS[direction] in PIPE_SHAPES[to_shape]
    return can_move_from and can_arrive_to

def next_direction(direction, to_shape):
    if to_shape == 'S':
        return None
    if to_shape == '|':
        return direction
    if to_shape == '-':
        return direction
    arrive_from_direction = OPPOSITE_DIRECTIONS[direction]
    return PIPE_SHAPES[to_shape].replace(arrive_from_direction, '')

def move(problem, position, direction):
    i, j = position
    di, dj = DIRECTIONS[direction]
    if 0 <= i + di < len(problem) and 0 <= j + dj < len(problem[0]):
        from_shape = problem[i][j]
        to_shape = problem[i + di][j + dj]
        if to_shape == '.':
            return None, None
        if compatible_shapes(from_shape, direction, to_shape):
            return (i + di, j + dj), next_direction(direction, to_shape)
    return None, None

def find_loop(problem, start, direction):
    position = start
    steps = []
    while True:
        position, direction = move(problem, position, direction)
        if position is None:
            return
        steps.append(position)
        if position == start:
            return steps

def solve(problem):
    start = find_start(problem)
    loop = next(filter(None, (find_loop(problem, start, direction) for direction in DIRECTIONS)))
    return (len(loop) + 1) // 2

print(solve(parse(sys.stdin)))