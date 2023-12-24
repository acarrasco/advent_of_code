import sys
from math import inf

def parse_line(line):
    position, velocity = line.split('@')
    return [int(p) for p in position.split(',')], [int(v) for v in velocity.split(',')]

def parse(lines):
    return [parse_line(line.strip()) for line in lines if line.strip()]

def collision(a, b):
    (ax, ay, _), (avx, avy, _) = a
    (bx, by, _), (bvx, bvy, _) = b
    
    v_factor = avy * bvx - avx * bvy
    if v_factor == 0:
        return inf, inf

    ta = -(bvx * (ay - by) + bvy*bx - ax * bvy) / v_factor

    tb = -(avx * (ay - by) + avy*bx - ax * avy) / v_factor

    if ta < 0 or tb < 0:
        return inf, inf
    
    x = ax + avx * ta
    y = ay + avy * ta

    return x, y

def solve(hailstones, target_area):
    min_target, max_target = target_area
    collisions = 0

    for i, a in enumerate(hailstones):
        for j in range(i+1, len(hailstones)):
            b = hailstones[j]
            x, y = collision(a, b)
            if min_target <= x <= max_target and min_target <= y <= max_target:
                collisions += 1
    
    return collisions

target_area = 200000000000000, 400000000000000
lines = sys.stdin.readlines()

print(solve(parse(lines), target_area))