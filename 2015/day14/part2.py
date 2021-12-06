from collections import defaultdict
import sys
import re

exp = '([a-zA-Z]+) can fly ([0-9]+) km/s for ([0-9]+) seconds, but then must rest for ([0-9]+) seconds.'


def parse_reindeer(line):
    name, speed, flying_time, resting_time = re.match(exp, line).groups()
    return name, int(speed), int(flying_time), int(resting_time)


def distance(reindeer, seconds):
    _name, speed, flying_time, resting_time = reindeer
    block_time = flying_time + resting_time
    block_distance = speed * flying_time

    whole_blocks = seconds // block_time
    remaining = seconds % block_time

    return whole_blocks * block_distance + min(remaining, flying_time) * speed


def all_max(iterable, key=lambda x: x):
    mx = None
    elements = []
    for i in iterable:
        v = key(i)
        if mx is None or v > mx:
            elements = [i]
            mx = v
        elif v == mx:
            elements.append(i)

    return elements

def calculate_points(reindeers, seconds):
    points = defaultdict(int)
    for time in range(1, seconds):
        winners = all_max(reindeers, lambda reindeer: distance(reindeer, time))
        for winner, *_ in winners:
            points[winner] += 1
    return points

def solve(seconds):
    reindeers = list(parse_reindeer(line) for line in sys.stdin.readlines())
    points = calculate_points(reindeers, seconds)
    return max(points.values())

print(solve(2503))
