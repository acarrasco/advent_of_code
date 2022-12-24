import sys
import re

DIRECTIONS = [
    (0, 1), # right
    (1, 0), # down
    (0, -1), # left
    (-1, 0), # up
]

DIRECTION_CHANGE = {
    'R': 1,
    'L': -1,
}

def parse():
    m, s = sys.stdin.read().split('\n\n')
    cols = max(map(len, m.split('\n')))
    padded = [line + ' ' * (cols - len(line)) for line in m.split('\n')]
    return padded, [int(x) if x not in ('L', 'R') else x for x in re.split('([LR])', s)]

def advance(mp, state, ins):
    pos, dir_idx = state
    
    if ins in DIRECTION_CHANGE:
        return pos, (dir_idx + DIRECTION_CHANGE[ins]) % len(DIRECTIONS)
    
    steps = ins
    last_i, last_j = i, j = pos
    di, dj = DIRECTIONS[dir_idx]
    while steps:
        next_i = (i + di) % len(mp)
        next_j = (j + dj) % len(mp[next_i])
        print((next_i, next_j,), steps, '"' + mp[next_i][next_j] + '"')
        if mp[next_i][next_j] == '#':
            break
        if mp[next_i][next_j] == '.':
            steps -= 1
            last_i, last_j = next_i, next_j
        i, j = next_i, next_j
    
    return (last_i, last_j), dir_idx

def solve(mp, instructions):
    # print('\n'.join(mp))
    # print(instructions)
    pos = (0, 0)
    dir_idx = 0

    for ins in instructions:
        print('pos', pos, 'dir', dir_idx, 'ins', ins)
        pos, dir_idx = advance(mp, (pos, dir_idx), ins)
    
    print('pos', pos, 'dir', dir_idx, 'ins', ins)
    
    i, j = pos
    return 1000 * (i + 1) + 4 * (j + 1) + dir_idx

print(solve(*parse()))