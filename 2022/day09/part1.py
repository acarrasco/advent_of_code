import sys

DIRECTIONS = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (1, 0),
    'D': (-1, 0),
}

def parse(line):
    direction, length = line.split()
    return DIRECTIONS[direction], int(length)

def update_tail(head_position, tail_position):
    hi, hj = head_position
    ti, tj = tail_position

    di = hi - ti
    dj = hj - tj
    if abs(di) + abs(dj) > 2:
        di = di // abs(di)
        dj = dj // abs(dj)
    else:
        if abs(di) > 1:
            di = di // abs(di)
        else:
            di = 0

        if abs(dj) > 1:
            dj = dj // abs(dj)
        else:
            dj = 0
    return ti + di, tj + dj

def solve(steps):
    hi, hj = 0, 0
    ti, tj = 0, 0
    tail_positions = set([(0, 0)])
    for (di, dj), length in steps:
        for _ in range(length):
            hi += di
            hj += dj
            ti, tj = update_tail((hi, hj), (ti, tj))
            tail_positions.add((ti, tj))
        
    return len(tail_positions)


# def test_update_tail(head_position, tail_position, expected):
#     res = update_tail(head_position, tail_position)
#     if res != expected:
#         print('ERROR', head_position, tail_position, expected, res)
#     else:
#         print('OK   ', head_position, tail_position, expected, res)

# test_update_tail((0, 1), (0, 0), (0, 0))
# test_update_tail((1, 1), (1, 1), (1, 1))
# test_update_tail((0, 2), (0, 0), (0, 1))
# test_update_tail((1, 1), (0, 0), (0, 0))
# test_update_tail((1, 2), (0, 0), (1, 1))
# test_update_tail((0, -2), (0, 0), (0, -1))
# test_update_tail((2, 1), (1, 2), (1, 2))
# test_update_tail((2, 0), (1, 2), (2, 1))

print(solve(map(parse, sys.stdin)))