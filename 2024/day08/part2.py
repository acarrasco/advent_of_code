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

                ni = ai
                nj = aj
                while 0 <= ni < n and 0 <= nj < m:
                    antinodes.add((ni, nj))
                    ni -= di
                    nj -= dj
                
                ni = bi
                nj = bj
                while 0 <= ni < n and 0 <= nj < m:
                    antinodes.add((ni, nj))
                    ni += di
                    nj += dj

    return len(antinodes)

print(solve(parse([line.strip() for line in sys.stdin if line.strip()])))