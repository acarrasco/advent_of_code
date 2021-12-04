import sys
import itertools

boxes = [map(int, line.split('x')) for line in sys.stdin.readlines()]

side_combination_indices = list(itertools.combinations(range(3), 2))
def ribbon(box):
    w, h, l = sorted(box)
    return 2 * w + 2 * h + w * h * l

print(sum(ribbon(box) for box in boxes))