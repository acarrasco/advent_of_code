import sys

SCORE_MATRIX = {
    'A': {
        'X': 3,
        'Y': 6,
        'Z': 0,
    },
    'B': {
        'X': 0,
        'Y': 3,
        'Z': 6,
    },
    'C': {
        'X': 6,
        'Y': 0,
        'Z': 3,
    }
}

PIECE_POINTS = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

def round_score(elf, me):
    return SCORE_MATRIX[elf][me] + PIECE_POINTS[me]

print(sum(round_score(*line.strip().split()) for line in sys.stdin.readlines() if line.strip()))