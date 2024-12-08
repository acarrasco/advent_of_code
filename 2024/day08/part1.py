import sys
import collections
import itertools

def parse(lines):
    antennas = collections.defaultdict(list)
    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell != '.':
                antennas[cell].append((i ,j))
    return antennas, (len(lines), len(lines[0]))

def solve(problem):
    antennas, (n, m) = problem
    antinodes = set()

    for antenna_type in antennas.values():
        for a, b in itertools.product(antenna_type, repeat=2):
            if a != b:
                ai, aj = a
                bi, bj = b
                di = bi - ai
                dj = bj - aj

                n1i = ai - di
                n1j = aj - dj
                n2i = bi + di
                n2j = bj + dj

                if 0 <= n1i < n and 0 <= n1j < m:
                    antinodes.add((n1i, n1j))
                if 0 <= n2i < n and 0 <= n2j < m:
                    antinodes.add((n2i, n2j))
    return len(antinodes)

print(solve(parse([line.strip() for line in sys.stdin if line.strip()])))