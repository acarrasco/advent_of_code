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

ROCK_COUNT = 1000000000000

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

    while not settled:
        dj = jets[step % len(jets)]
        if 0 <= j + dj and j + w + dj <= WIDTH and not (cave[i:i+h, j+dj:j+dj+w] * rock_shape).any():
            j += dj
        step += 1
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

def cave_top(cave):
    flood = ['+' * WIDTH]
    i = 0
    while True:
        i += 1
        cond = list(zip(flood[-1], ' ' + flood[-1][:-1], flood[-1][1:] + ' ', cave[i]))
        #print(cond)
        new = ''.join('+' if r == 0 and '+' in (a, b, c) else ' ' for a, b, c, r in cond)
        if '+' in new:
            flood.append(new)
        else:
            break
    return '\n'.join(flood)

def pile_height(cave):
    space_available = 0
    while not sum(cave[space_available]):
        space_available += 1
    return len(cave) - 1 - space_available # discount the floor sentinel

def format_cave(cave, i=None, j=None):
    return '\n'.join(''.join('.#@-'[c] for c in row) for row in cave[i:j])

CAVE_FLOOR = [3]*WIDTH # a sentinel to simplify rock fall check

jets = parse_input(sys.stdin.read())
cycle_factor = len(jets) * len(ROCKS)

cave = numpy.array([CAVE_FLOOR])
step = 0

snapshots = []
heights = []
rock_index = 0
cycle_size = 0
while not cycle_size:
    cave = resize_cave(cave, len(ROCKS[rock_index % len(ROCKS)]))
    cave, step = rock_fall(jets, step, cave, rock_index, (0, 2))
    heights.append(pile_height(cave))
    snapshots.append(cave_top(cave))

    for k in range(len(snapshots) // cycle_factor):
        if snapshots[-1] == snapshots[-cycle_factor * k - 1]:
            cycle_size = k * cycle_factor
    rock_index += 1

print(rock_index, cycle_size, heights[-cycle_size-1], heights[-1])

remaining_rocks = ROCK_COUNT - rock_index
remaining_chunks = remaining_rocks // cycle_size
chunk_height = heights[-1] - heights[-cycle_size-1]
chunks_remainder = remaining_rocks % cycle_size
whole_chunks_height = chunk_height * remaining_chunks
chunks_remainder_height = heights[-cycle_size - 1 + chunks_remainder] - heights[-cycle_size-1]
total_height = heights[-1] + whole_chunks_height + chunks_remainder_height

print({
'rock_index': rock_index,
'remaining_rocks': remaining_rocks,
'remaining_chunks': remaining_chunks,
'chunk_height': chunk_height,
'chunks_remainder': chunks_remainder,
'whole_chunks_height': whole_chunks_height,
'chunks_remainder_height': chunks_remainder_height,
'total_height': total_height,
})

print(total_height)
