import sys
from collections import namedtuple

State = namedtuple('State', 'i j d s'.split())

def a_star(start, is_goal, neighbors, d, h):
    from math import inf
    from collections import defaultdict
    import heapq

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)

    open_set = [(f_score[start], start)]

    while open_set:
        _, current = heapq.heappop(open_set)
        if is_goal(current):
            return g_score[current]

        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + d(current, neighbor)
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                fs = tentative_g_score + h(neighbor)
                if fs != inf:
                    f_score[neighbor] = fs
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

LEFT = {
    NORTH: WEST,
    WEST: SOUTH,
    SOUTH: EAST,
    EAST: NORTH
}

RIGHT = {v:k for k, v in LEFT.items()}

MAX_STRAIGHT_STEPS = 2 # discount current

def simulate(problem):
    rows, cols = len(problem), len(problem[0])

    def inside(i, j):
        return 0 <= i < rows and 0 <= j < cols

    def neighbors(state):
        i, j, d, s = state.i, state.j, state.d, state.s

        if not d:
            for di, dj in [SOUTH, EAST]:
                yield State(i=i+di, j=j+dj, d=(di, dj), s=MAX_STRAIGHT_STEPS)
            return

        # straight
        if s > 0:
            di, dj = d
            ni, nj = i + di, j + dj
            if inside(ni, nj): 
                yield State(i=ni, j=nj, d=d, s=s - 1)

        # left
        li, lj = LEFT[d]
        ni, nj = i + li, j + lj
        if inside(ni, nj):
            yield State(i=ni, j=nj, d=(li, lj), s=MAX_STRAIGHT_STEPS)
        # right
        ri, rj = RIGHT[d]
        ni, nj = i + ri, j + rj
        if inside(ni, nj):
            yield State(i=ni, j=nj, d=(ri, rj), s=MAX_STRAIGHT_STEPS)

    def d(_current, neighbor):
        return problem[neighbor.i][neighbor.j]

    def h(state):
        return ((rows - state.i) + (cols - state.j))
    
    def is_goal(state):
        return state.i == rows - 1 and state.j == cols - 1

    return a_star(State(i=0, j=0, d=None, s=None), is_goal, neighbors, d, h)


def parse_line(line):
    return [int(x) for x in line.strip()]

def parse(lines):
    return [parse_line(line) for line in lines]

def solve(problem):
    solution = simulate(problem)
    return solution

input = sys.stdin.readlines()
print(solve(parse(input)))