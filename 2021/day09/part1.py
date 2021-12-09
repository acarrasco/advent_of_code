import sys

neighbors = [(i, j) for i in (-1, 0, 1)
             for j in (-1, 0, 1) if bool(i) ^ bool(j)]
print(neighbors)


def parse_line(line):
    return list(map(int, line.strip()))


input = list(map(parse_line, sys.stdin.readlines()))


def get_neighbors(table, i, j):
    for di, dj in neighbors:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(table) and 0 <= nj < len(table[ni]):
            yield table[ni][nj]


def is_low(table, i, j):
    depth = table[i][j]
    return all(nd > depth for nd in get_neighbors(table, i, j))


def risk_level(table, i, j):
    return is_low(table, i, j) and table[i][j] + 1 or 0


print(sum(risk_level(input, i, j) for i in range(len(input))
      for j in range(len(input[i]))))
