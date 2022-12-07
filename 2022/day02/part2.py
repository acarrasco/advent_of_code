import sys

PIECE_MATRIX = {
    'A': {
        'X': 3,
        'Y': 1,
        'Z': 2,
    },
    'B': {
        'X': 1,
        'Y': 2,
        'Z': 3,
    },
    'C': {
        'X': 2,
        'Y': 3,
        'Z': 1,
    }
}

SCORE_POINTS = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}

def round_score(a, b):
    return PIECE_MATRIX[a][b] + SCORE_POINTS[b]

print(sum(round_score(*line.strip().split()) for line in sys.stdin.readlines() if line.strip()))