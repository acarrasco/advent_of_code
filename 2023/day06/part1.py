import sys


def parse(lines):
    times = map(int, lines[0].split(':')[1].split())
    distances =  map(int, lines[1].split(':')[1].split())

    return list(zip(times, distances))

def calculate_race_distance(charge_time, race_time):
    speed = charge_time
    remaining_time = race_time - charge_time
    return speed * remaining_time

def calculate_ways_to_beat(time, distance):
    ways = 0
    for charging_time in range(1, time):
        my_distance = calculate_race_distance(charging_time, time)
        if my_distance > distance:
            ways += 1
    return ways

def solve(problem):
    result = 1
    for time, distance in problem:
        result *= calculate_ways_to_beat(time, distance)

    return result


print(solve(parse(sys.stdin.readlines())))
