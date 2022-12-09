import sys

DIRECTIONS = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (1, 0),
    'D': (-1, 0),
}

ROPE_LENGTH = 10

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
    tail_positions = set([(0, 0)])
    rope_positions = [(0, 0) for _ in range(ROPE_LENGTH)]
    for (di, dj), length in steps:
        for _ in range(length):
            hi, hj = rope_positions[0]
            rope_positions[0] = (hi + di, hj + dj)
            for n in range(ROPE_LENGTH - 1):
                hi, hj = rope_positions[n]
                ti, tj = rope_positions[n+1]
                rope_positions[n] = (hi, hj)
                rope_positions[n+1] = update_tail((hi, hj), (ti, tj))                
        
            tail_positions.add(rope_positions[-1])
        
    return len(tail_positions)


print(solve(map(parse, sys.stdin)))