import sys
import heapq

neighbors = [(i, j) for i in (-1, 0, 1)
             for j in (-1, 0, 1) if bool(i) ^ bool(j)]


def parse_line(line):
    return list(map(int, line.strip()))


input = list(map(parse_line, sys.stdin.readlines()))


def get_neighbors(table, i, j):
    for di, dj in neighbors:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(table) and 0 <= nj < len(table[ni]):
            yield ni, nj


def is_low(table, i, j):
    depth = table[i][j]
    return all(table[ni][nj] > depth for ni, nj in get_neighbors(table, i, j))


def find_basin(table, i, j, points):
    for ni, nj in get_neighbors(table, i, j):
        if table[ni][nj] != 9 and (ni, nj) not in points:
            points.add((ni, nj))
            find_basin(table, ni, nj, points)
    return points


def basin_size(table, i, j):
    points = find_basin(table, i, j, set())
    # print(i, j)
    # print_region(table, points)
    return len(points)


def find_basin_sizes(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            if is_low(table, i, j):
                yield basin_size(table, i, j)


def mul(seq):
    m = 1
    for i in seq:
        m *= i
    return m


def print_region(table, points):
    for i, line in enumerate(table):
        print(''.join((i, j) in points and '*' or str(v)
              for j, v in enumerate(line)))
    print()


print(mul(heapq.nlargest(3, find_basin_sizes(input))))
