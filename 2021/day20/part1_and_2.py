import sys


def parse_algo(line):
    return [int(x == '#') for x in line]


def parse_image(lines):
    img = set()
    for i, line in enumerate(lines):
        for j, pixel in enumerate(line):
            if pixel == '#':
                img.add((i, j))
    return img


class Inverted:
    def __init__(self):
        self.img = set()

    def __contains__(self, p):
        return p not in self.img

    def add(self, p):
        self.img.add(p)

    def __iter__(self):
        return iter(self.img)


def enhance_image(algo, image, inverted):
    def pixel_neighbours(i, j):
        for di in range(-1, 2):
            for dj in range(-1, 2):
                yield '01'[inverted ^ ((i+di, j+dj) in image)]

    def read_pixel(i, j):
        return int(''.join(pixel_neighbours(i, j)), 2)

    res = set()
    (min_i, min_j), (max_i, max_j) = image_boundaries(image, inverted)
    invert = algo[0]
    for i in range(min_i-1, max_i+2):
        for j in range(min_j-1, max_j+2):
            p = read_pixel(i, j)
            lit = algo[p]
            if lit ^ invert ^ inverted:
                res.add((i, j))

    return res, invert ^ inverted


def parse(lines):
    algo = parse_algo(lines[0])
    image = parse_image(lines[2:])
    return algo, image


def image_boundaries(image, inverted=False):
    inf = float('inf')
    min_i = inf
    max_i = -inf
    min_j = inf
    max_j = -inf
    for i, j in image:
        min_i = min(min_i, i)
        max_i = max(max_i, i)
        min_j = min(min_j, j)
        max_j = max(max_j, j)
    min_i -= inverted
    min_j -= inverted
    max_i += inverted
    max_j += inverted
    return (min_i, min_j), (max_i, max_j)


def print_image(image, inverted=False):
    (min_i, min_j), (max_i, max_j) = image_boundaries(image, inverted)

    pad = inverted and 'o' or ''
    print(pad * (3+max_j - min_j))
    for i in range(min_i, max_i+1):
        print(pad + ''.join('.#'[inverted ^ ((i, j) in image)] for j in range(min_j, max_j+1)) + pad)
    print(pad * (3+max_j - min_j))


def enhance_loop(algo, image, times):
    enhanced = image
    inverted = False
    for i in range(times):
        # print()
        enhanced, inverted = enhance_image(algo, enhanced, inverted)
        #print_image(enhanced, inverted)
    return enhanced


algo, image = parse(sys.stdin.readlines())
times = int(sys.argv[1])


print(len(enhance_loop(algo, image, times)))
