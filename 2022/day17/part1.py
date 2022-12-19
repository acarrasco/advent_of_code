import sys
import numpy

DASH_SHAPE = [[1, 1, 1, 1]]

CROSS_SHAPE = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

L_SHAPE = [
    [0, 0, 1],
    [0, 0, 1],
    [1, 1, 1],
]

BAR_SHAPE = [
    [1],
    [1],
    [1],
    [1],
]

BOX_SHAPE = [
    [1, 1],
    [1, 1],
]

ROCKS =[numpy.array(shape) for shape in [
    DASH_SHAPE,
    CROSS_SHAPE,
    L_SHAPE,
    BAR_SHAPE,
    BOX_SHAPE,
]]

WIDTH = 7

def parse_input(line):
    translate = {
        '<': -1,
        '>': 1,
    }
    return [translate[i] for i in line.strip()]

def rock_fall(jets, step, cave, rock_index, rock_position):
    i, j = rock_position

    rock_shape = ROCKS[rock_index % len(ROCKS)]
    h, w = rock_shape.shape
    
    settled = False
    # print()
    # print_cave(cave, rock_index, rock_position)
    # print()

    while not settled:
        dj = jets[step % len(jets)]
        # print_cave(cave, rock_index, (i, j))
        # print({-1:'<', 1:'>'}[dj])
        if 0 <= j + dj and j + w + dj <= WIDTH and not (cave[i:i+h, j+dj:j+dj+w] * rock_shape).any():
            j += dj
        step += 1
        #print_cave(cave, rock_index, (i, j))
        # print('v')
        settled = (cave[i+1:i+1+h, j:j+w] * rock_shape).any()
        if not settled:
            i += 1
    

    cave[i:i+h, j:j+w] += rock_shape
    return cave, step

def resize_cave(cave, rock_height):
    space_available = 0
    while not sum(cave[space_available]):
        space_available += 1

    space_needed = 3 + rock_height
    
    if space_needed == 0:
        return cave
    elif space_needed > space_available:
        padding = [[0] * WIDTH] * (space_needed - space_available)
        return numpy.concatenate((padding, cave))
    else:
        remove_from = space_available - space_needed
        return cave[remove_from:]

def pile_height(cave):
    space_available = 0
    while not sum(cave[space_available]):
        space_available += 1
    return len(cave) - 1 - space_available # discount the floor sentinel

def print_cave(cave, rock_index=None, rock_position=None):
    if rock_index or rock_position:
        cave = cave.copy()
        i, j = rock_position
        rock_shape = ROCKS[rock_index % len(ROCKS)]
        h, w = rock_shape.shape
        cave[i:i+h, j:j+w] = rock_shape * 2
    for row in cave:
        print(''.join('.#@-'[c] for c in row))

jets = parse_input(sys.stdin.read())
CAVE_FLOOR = [3]*WIDTH # a sentinel to simplify rock fall check

cave = numpy.array([CAVE_FLOOR])
step = 0
for rock_index in range(2022):
    cave = resize_cave(cave, len(ROCKS[rock_index % len(ROCKS)]))
    cave, step = rock_fall(jets, step, cave, rock_index, (0, 2))

# print_cave(cave)
# print()
print(pile_height(cave))