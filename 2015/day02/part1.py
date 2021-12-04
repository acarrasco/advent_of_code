import sys
import itertools

boxes = [map(int, line.split('x')) for line in sys.stdin.readlines()]

side_combination_indices = list(itertools.combinations(range(3), 2))
def wrapping_paper(box):
    faces = [box[i] * box[j] for i, j in side_combination_indices]
    slack = min(faces)
    return slack + sum(2 * face for face in faces)

print(sum(wrapping_paper(box) for box in boxes))