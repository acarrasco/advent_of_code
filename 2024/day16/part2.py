import sys
from math import inf
from collections import defaultdict, namedtuple

DIRECTIONS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]

def sign(x):
    return x and x // abs(x)

def parse(lines):
    start = None
    end = None
    walls = set()
    for i, row in enumerate(lines):
        for j, c in enumerate(row):
            if c == 'S':
                start = i, j
            elif c == 'E':
                end = i, j
            elif c == '#':
                walls.add((i, j))
    return walls, start, end

def a_star(start, is_goal, neighbors, d, h):
    from math import inf
    from collections import defaultdict
    import heapq

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)

    open_set = [(f_score[start], start)]

    ancestors = defaultdict(set)

    while open_set:
        _, current = heapq.heappop(open_set)
        if is_goal(current):
            yield g_score[current], current, ancestors

        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + d(current, neighbor)
            if tentative_g_score < g_score[neighbor]:
                ancestors[neighbor].clear()
            if tentative_g_score <= g_score[neighbor]:
                ancestors[neighbor].add(current)
                g_score[neighbor] = tentative_g_score
                fs = tentative_g_score + h(neighbor)
                if fs != inf:
                    f_score[neighbor] = fs
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

def print_seats(walls, seats):
    max_row, _ = max(walls)
    cols = max(j for _, j in walls)

    for i in range(max_row + 1):
        print(''.join((i,j) in seats and 'O' or
                      (i,j) in walls and '#' or
                      '.'
                      for j in range(cols + 1)))

State = namedtuple('State', ['position', 'facing'])
def solve(problem):
    walls, start, end = problem
    
    def is_goal(state):
        return end == state.position

    def h(state):
        cost = 0
        i, j = state.position
        facing = state.facing
        end_i, end_j = end
        
        facing_i, facing_j = DIRECTIONS[facing]
        di = end_i - i
        dj = end_j - j

        cost += 1000 * abs(sign(di) - sign(facing_i))
        cost += 1000 * abs(sign(dj) - sign(facing_j))
        cost += abs(end_i - i) + abs(end_j - j)

        return cost

    def neighbors(state):
        i, j = state.position
        facing = state.facing
        di, dj = DIRECTIONS[facing]
        
        ni = i + di
        nj = j + dj
        if (ni, nj) not in walls:
            yield State((ni, nj), facing)

        yield State((i, j), (facing + 1) % 4)
        yield State((i, j), (facing - 1) % 4)

    def d(current, neighbor):
        ci, cj = current.position
        ni, nj = neighbor.position
        cf = current.facing
        nf = neighbor.facing

        r = abs(ci - ni) + abs(cj - nj) + 1000 * (cf != nf)
        return r

    seats = set()
    def add_seats(current, ancestors):
        pending = [current]
        seen = set()
        while pending:
            current = pending.pop()
            if current not in seen:
                seen.add(current)
                seats.add(current.position)
                for a in ancestors[current]:
                    pending.append(a)
    
    best_score = inf
    for score, state, ancestors in (a_star(State(start, 0), is_goal, neighbors, d, h)):
        if score <= best_score:
            print(score)
            best_score = score
            add_seats(state, ancestors)
        else:
            break
    print_seats(walls, seats)
    return len(seats)

print(solve(parse(sys.stdin)))
