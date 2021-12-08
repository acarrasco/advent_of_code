import sys

ADJACENCY = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j]


def parse(lines):
    return [
        [c == '#' and 1 or 0 for c in line.strip()]
        for line in lines
    ]


def get_neighbours(grid, i, j):
    for di, dj in ADJACENCY:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[ni]):
            yield grid[ni][nj]


def rule(light, lit_neightbors):
    if light:
        after = int(2 <= lit_neightbors <= 3)
    else:
        after = int(lit_neightbors == 3)
    return after


def cycle(lights):
    return [
        [rule(lights[i][j], sum(get_neighbours(lights, i, j)))
         for j in range(len(lights[i]))]
        for i in range(len(lights))
    ]


def pretty(lights, clear = True):
    clr = clear and (chr(27)+'[2j\n' +
             '\033c\n' +
             '\x1bc\n'
             ) or ''

    return clr + '\n'.join(
        ''.join(light and '#' or '.' for light in line)
        for line in lights
    ) + '\n'


def simulate(lights, cycles):
    for i in range(1, cycles+1):
        lights = cycle(lights)
        print(pretty(lights))
        print(i, how_many_lit(lights))

    return lights


def how_many_lit(lights):
    return sum(map(sum, lights))


input = parse(sys.stdin.readlines())
cycles = int(sys.argv[1])
after_cycles = simulate(input, cycles)
#print(how_many_lit(after_cycles))
