import sys
from collections import defaultdict


inf = float('inf')

adjacency = [(i, j) for i in (-1, 0, 1)
             for j in (-1, 0, 1) if i or j]


def parse_line(line):
    return [int(x) for x in line.strip()]


def increase_all(input):
    return [[energy + 1 for energy in row] for row in input]


def increase_flashed(input, been_flashed_times):
    return [[energy + been_flashed_times[i, j]
             for j, energy in enumerate(row)]
            for i, row in enumerate(input)]


def reset_flashed(input):
    return [[max(0, energy) for energy in row] for row in input]


def get_neighbors(i, j, rows, columns):
    for di, dj in adjacency:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= j <= columns:
            yield ni, nj


def flash(input):
    been_flashed_times = defaultdict(int)
    copy = [row[:] for row in input]
    for i, row in enumerate(copy):
        for j, energy in enumerate(row):
            if energy > 9:
                for ni, nj in get_neighbors(i, j, len(copy), len(row)):
                    been_flashed_times[ni, nj] += 1
                    copy[i][j] = -inf
    return been_flashed_times, copy


def step(input):
    next_step = increase_all(input)
    finished = False
    while not finished:
        been_flashed_times, next_step = flash(next_step)
        finished = len(been_flashed_times) == 0
        next_step = increase_flashed(next_step, been_flashed_times)

    flashed_this_step = sum(energy == -inf for row in next_step for energy in row)
    return reset_flashed(next_step), flashed_this_step


def solve(input):
    s = 0
    input_size = sum(map(len, input))
    while True:
        s += 1
        input, new_flashes = step(input)
        if new_flashes == input_size:
            return s


input = sys.stdin

problem = [parse_line(line) for line in input.readlines()]
print(solve(problem))
