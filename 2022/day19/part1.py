import sys
import re

def parse(line):
    tokens = line.strip().split()
    blueprint = {
        'geode': {
            'ore': int(tokens[27]),
            'obsidian': int(tokens[30]),
        },
        'obsidian': {
            'ore': int(tokens[18]),
            'clay': int(tokens[21]),
        },
        'clay': {
            'ore': int(tokens[12]),
        },
        'ore': {
            'ore': int(tokens[6]),            
        },
    }
    return int(tokens[1][:-1]), blueprint

def try_build_robot(blueprint, robot, state):
    robots, resources, time = state
    requirements = blueprint[robot]
    t = 0
    for res, quantity_needed in requirements.items():
        if not robots[res]:
            return None
        remaining = quantity_needed - resources[res]
        t = max(t, remaining // robots[res] + bool(remaining % robots[res]))
    
    if t >= time:
        return None

    new_robots = {
        **robots, robot: robots[robot] + 1
    }

    new_resources = {
        r: q + (t + 1) * robots[r] - blueprint[robot].get(r, 0)  for r, q in resources.items()
    }
    
    return new_robots, new_resources, time - t - 1

def max_geodes(blueprint, state, cache):

    if state is None:
        return None

    strstate = str(state)
    if strstate in cache:
        return cache[strstate]

    robots, resources, time = state
    if time < 0:
        return None

    if time == 0:
        return resources['geode']

    r = max(
        filter(None, (max_geodes(blueprint, try_build_robot(blueprint, robot, state), cache) for robot in blueprint)),
        default=resources['geode'] + time * robots['geode']
    )
    cache[strstate] = r
    return r

def quality(parsed):
    blueprint_index, blueprint = parsed
    starting_robots = {
        'ore': 1,
        'clay': 0,
        'obsidian': 0,
        'geode': 0,
    }
    starting_resources = {
        'ore': 0,
        'clay': 0,
        'obsidian': 0,
        'geode': 0,
    }
    m = max_geodes(blueprint, (starting_robots, starting_resources, 24), {})
    return blueprint_index * m

print(sum(quality(parse(line)) for line in sys.stdin))
