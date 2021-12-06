import sys
import numpy
import itertools

SIZE = 5

agg_cols = numpy.matrix([1] * SIZE)
agg_rows = agg_cols.transpose()


def build_board_index(board):
    return {v: (i, j) for (i, row) in enumerate(board) for (j, v) in enumerate(row)}


def read_boards(board_lines):
    board = []
    for line in board_lines:
        line = line.strip()
        if line:
            board.append(list(map(int, line.split())))
        else:
            yield numpy.matrix(board), build_board_index(board)
            board = []


def mark_board(board_index, ball):
    board, index = board_index
    pos = index.pop(ball, None)
    if pos:
        board[pos] = -1
        if not ((board >= 0) * agg_rows).all() or not (agg_cols * (board >= 0)).all():
            index.clear()
            return board[board >= 0].sum() * ball
    return -1


lines = sys.stdin.readlines()

numbers = map(int, lines[0].split(','))

boards_and_indices = list(read_boards(lines[2:]))

winners = filter(lambda x: x >= 0, ((mark_board(bi, n)) for n in numbers for bi in boards_and_indices))
*_, last = winners
print(last)