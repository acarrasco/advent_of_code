import sys

NUM_KEYPAD = [
    '789',
    '456',
    '123',
    ' 0A',
]

NUM_KEYPAD_POSITIONS = {k: (i, j) for i, row in enumerate(NUM_KEYPAD) for j, k in enumerate(row)}

DIRECTIONAL_KEYPAD = [
    ' ^A',
    '<v>'
]

DIRECTIONAL_KEYPAD_POSITIONS = {k: (i, j) for i, row in enumerate(DIRECTIONAL_KEYPAD) for j, k in enumerate(row)}

DIRECTIONS = {
    '^': (-1, 0),
    'v': (1, 0),
    '>': (0, 1),
    '<': (0, -1),
}

RANK = '<v>^'

DIRECTIONS_KEYS = {
    (-1, 0): '^',
    (1, 0): 'v',
    (0, 1): '>',
    (0, -1): '<',
}

def parse_line(line):
    return line.strip()

def calculate_movement_cursors(keyboard_positions, start, end):
    i, j = start
    ei, ej = end
    gi, gj = keyboard_positions[' ']

    di, dj = ei - i, ej - j

    if i == gi and ej == gj:
        for k in range(abs(di)):
            yield DIRECTIONS_KEYS[di // abs(di), 0]
        for k in range(abs(dj)):
            yield DIRECTIONS_KEYS[0, dj // abs(dj)]
    elif j == gj and ei == gi:
        for k in range(abs(dj)):
            yield DIRECTIONS_KEYS[0, dj // abs(dj)]
        for k in range(abs(di)):
            yield DIRECTIONS_KEYS[di // abs(di), 0]
    else:
        movements = [
                DIRECTIONS_KEYS[di // abs(di), 0] for _ in range(abs(di))
            ] + [
                DIRECTIONS_KEYS[0, dj // abs(dj)] for _ in range(abs(dj))
        ]
        yield from sorted(movements, key=RANK.index)


def robot_movements(keyboard_positions, start_key, key_sequence):
    position = keyboard_positions[start_key]
    key = start_key

    for next_key in key_sequence:
        next_position = keyboard_positions[next_key]
        yield from calculate_movement_cursors(keyboard_positions, position, next_position)
        yield 'A'
        position = next_position
        key = next_key

def simulate_robot(key_positions, start_key, movements):
    i, j = key_positions[start_key]
    gap = key_positions[' ']
    for m_idx, m in enumerate(movements):
        if (i, j) == gap:
            raise Exception('went over a gap', ''.join(
                ''.join(movements[:m_idx] + ['*'] + movements[m_idx:])
            ))
        if m == 'A':
            yield next(k for k, v in key_positions.items() if v == (i, j))
        else:
            di, dj = DIRECTIONS[m]
            i += di
            j += dj

def parse(lines):
    return [parse_line(line) for line in lines]

def solve(problem):
    total = 0

    for l0 in problem:
        l1 = list(robot_movements(NUM_KEYPAD_POSITIONS, 'A', l0))
        l2 = list(robot_movements(DIRECTIONAL_KEYPAD_POSITIONS, 'A', l1))
        l3 = list(robot_movements(DIRECTIONAL_KEYPAD_POSITIONS, 'A', l2))
        n = int(l0[:-1])
        k = sum(1 for _ in l3)
        print(''.join(l3))
        print(''.join(l2))
        print(''.join(l1))
        print(l0, k, n)
        r2 = list(simulate_robot(DIRECTIONAL_KEYPAD_POSITIONS, 'A', l3))
        r1 = list(simulate_robot(DIRECTIONAL_KEYPAD_POSITIONS, 'A', r2))
        r0 = list(simulate_robot(NUM_KEYPAD_POSITIONS, 'A', r1))
        if r0 != list(l0) or r1 != l1 or r2 != l2:
            raise Exception('mismatched simulation',
                            (l0, r0),
                            (l1, r1),
                            (l2, r2),
                            )
        print()
        total += n * k
    return total

print(solve(parse(sys.stdin)))
