import sys
import argparse

DIRECTIONS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]

def parse_line(line):
    j, i = [int(x) for x in line.split(',')]
    return i, j

def parse(lines):
    return [parse_line(line) for line in lines]

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

def solve(problem, fallen_bytes, rows, cols):
    
    end = rows-1, cols-1

    walls = set(b for _, b in zip(range(fallen_bytes), problem))

    def is_goal(state):
        return end == state

    def h(state):
        i, j = state
        end_i, end_j = end

        cost = abs(end_i - i) + abs(end_j - j)

        return cost

    def neighbors(state):
        i, j = state
        for di, dj in DIRECTIONS:
            ni = i + di
            nj = j + dj

            if 0 <= ni < rows and 0 <= nj < cols and (ni, nj) not in walls:
                yield (ni, nj)

    def d(current, neighbor):
        ci, cj = current
        ni, nj = neighbor

        r = abs(ci - ni) + abs(cj - nj)
        return r

    return a_star((0, 0), is_goal, neighbors, d, h)

parser = argparse.ArgumentParser()
parser.add_argument('--bytes', type=int, default=1024)
parser.add_argument('--rows', type=int, default=71)
parser.add_argument('--cols', type=int, default=71)
args = parser.parse_args()

print(solve(parse(sys.stdin), args.bytes, args.rows, args.cols))
