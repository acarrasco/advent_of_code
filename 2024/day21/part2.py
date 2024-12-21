import sys
import argparse
from functools import cache

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

def parse_line(line):
    return line.strip()

def all_movement_cursors(keyboard_positions, start, end, current=''):
    i, j = start
    ei, ej = end
    gap = keyboard_positions[' ']

    if start == gap:
        return

    if start == end:
        yield current
        return
    
    di = ei - i
    dj = ej - j

    if di > 0:
        yield from all_movement_cursors(keyboard_positions, 
                                        (i + 1, j),
                                        end,
                                        current + 'v')
    if di < 0:
        yield from all_movement_cursors(keyboard_positions, 
                                        (i - 1, j),
                                        end,
                                        current + '^')
    if dj > 0:
        yield from all_movement_cursors(keyboard_positions, 
                                        (i, j + 1),
                                        end,
                                        current + '>')
    if dj < 0:
        yield from all_movement_cursors(keyboard_positions, 
                                        (i, j - 1),
                                        end,
                                        current + '<')

@cache
def count_movements(start_key, end_key, depth, top=False):
    keyboard_positions = top and NUM_KEYPAD_POSITIONS or DIRECTIONAL_KEYPAD_POSITIONS
    position = keyboard_positions[start_key]
    end_position = keyboard_positions[end_key]

    if depth == 0:
        return 1

    min_cost = float('inf')
    for movements in all_movement_cursors(keyboard_positions, position, end_position):
        cost = 0
        lower_level_prev = 'A'
        for m in movements:
            cost += count_movements(lower_level_prev, m, depth - 1)
            lower_level_prev = m
        cost += count_movements(lower_level_prev, 'A', depth - 1)
        if cost < min_cost:
            min_cost = cost
    print(f'depth {depth} from {start_key} to {end_key} cost {min_cost}')
    return min_cost

def parse(lines):
    return [parse_line(line) for line in lines]

def solve(problem, robots):
    total = 0

    for code in problem:
        k = 0
        for a, b in zip('A' + code, code):
            k += count_movements(a, b, robots + 1, top=True)
        n = int(code[:-1])
        print(code, k, n)
        total += n * k

    return total

parser = argparse.ArgumentParser()
parser.add_argument('--robots', type=int, default=25)
args = parser.parse_args()

print(solve(parse(sys.stdin), args.robots))
