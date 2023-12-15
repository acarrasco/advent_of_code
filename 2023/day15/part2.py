import sys
import re

def parse_line(line):
    return line.split(',')

def parse(lines):
    return parse_line(lines[0].strip())

def my_hash(txt):
    v = 0
    for c in txt:
        v += ord(c)
        v *= 17
        v %= 256
    return v

def calculate_focusing_power(boxes):
    total_power = 0
    for i, box in enumerate(boxes):
        box_power = 0
        for j, (_, focal_length) in enumerate(box):
            box_power += (j + 1) * focal_length
        total_power += (i + 1) * box_power
    return total_power

def solve(problem):
    boxes = [[] for _ in range(256)]
    for step in problem:
        label, command, focal_length = re.split('(=|-)', step + ' ')
        box_index = my_hash(label)
        box = boxes[box_index]
        lens_index_to_remove = next((i for (i, (l, _)) in enumerate(box) if l == label), -1)
        if command == '-':
            if lens_index_to_remove >= 0:
                del box[lens_index_to_remove]
        elif command == '=':
            focal_length = int(focal_length)
            if lens_index_to_remove >= 0:
                box[lens_index_to_remove] = (label, focal_length)
            else:
                box.append((label, focal_length))
    return calculate_focusing_power(boxes)

print(solve(parse(sys.stdin.readlines())))