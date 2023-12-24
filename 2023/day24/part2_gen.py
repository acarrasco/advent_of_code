import sys

def parse_line(line):
    position, velocity = line.split('@')
    return [int(p) for p in position.split(',')], [int(v) for v in velocity.split(',')]

def parse(lines):
    return [parse_line(line.strip()) for line in lines if line.strip()]

def hailstone_equations(i, hailstone):
    (x, y, z), (vx, vy, vz) = hailstone
    return f'{x} + ({vx})*t{i} = rx + rvx * t{i}, {y} + ({vy})*t{i} = ry + rvy * t{i}, {z} + ({vz})*t{i} = rz + rvz * t{i}'

def generate_maxima_equations(hailstones, necessary=3):
    hs = hailstones[:necessary]
    print('solve([')
    print(',\n'.join(hailstone_equations(i, h) for i, h in enumerate(hs)))
    print('], [')
    print('rx, ry, rz, rvx, rvy, rvz,')
    print(', '.join(f't{i}' for i in range(necessary)))
    print(']);')
    print('quit();')

lines = sys.stdin.readlines()
generate_maxima_equations(parse(lines))