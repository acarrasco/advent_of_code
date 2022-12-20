import sys
import re
from math import inf

def parse(line):
    t = line.strip().split()
    return (
        (int(t[6]), 0, 0, 0),
        (int(t[12]), 0, 0, 0),
        (int(t[18]), int(t[21]), 0, 0),
        (int(t[27]), 0, int(t[30]), 0),
    )

def try_build_robot(blueprint, robot, state):
    robots, resources, time = state
    requirements = blueprint[robot]
    t = 0
    for res, quantity_needed in enumerate(requirements):
        if not quantity_needed:
            continue
        if robots[res] == 0:
            return None
        missing_res = quantity_needed - resources[res]
        t = max(t, missing_res // robots[res] + bool(missing_res % robots[res]))
    
    if t >= time:
        return None

    new_robots = tuple(rq + (ri == robot) for ri, rq in enumerate(robots))
    new_resources = tuple(
        q + (t + 1) * robots[r] - blueprint[robot][r] for r, q in enumerate(resources)
    )

    return new_robots, new_resources, time - t - 1

def max_geodes(blueprint, max_needed, state, cache):
    if state is None:
        return None

    state_key = str(state)
    if state_key in cache:
        return cache[state_key]

    robots, resources, time = state

    if time < 0:
        return None

    if time == 0:
        return resources[3]

    if all(r >= n for r, n in zip(robots[:-1], max_needed)):
        r = resources[3] + (time * time - 1) * robots[3] // 2
        cache[state_key] = r
        return r

    r = max(
        filter(None, (max_geodes(blueprint, max_needed, try_build_robot(blueprint, robot, state), cache) for robot in range(4)
            if robots[robot] < max_needed[robot])),
        default=resources[3] + time * robots[3]
    )
    cache[state_key] = r
    return r

def solve(blueprint):
    starting_robots = (1, 0, 0, 0)
    starting_resources = (0, 0, 0, 0)
    max_needed = [max(x) for x in zip(*blueprint)]
    max_needed[-1] = inf
    m = max_geodes(blueprint, max_needed, (starting_robots, starting_resources, 32), {})
    return m

p = 1
for line in sys.stdin.readlines()[:3]:
    p *= solve(parse(line))

print(p)
