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


print(max(distance(parse_reindeer(line), 2503) for line in sys.stdin.readlines()))
