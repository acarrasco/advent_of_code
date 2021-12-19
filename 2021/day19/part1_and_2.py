import sys
import itertools
import functools
from collections import defaultdict
from pprint import pprint


verbose = False


def dbg(*args):
    if verbose:
        pprint(args)


def not_empty(s):
    return s.strip()


def parse_coordinates(line):
    v = line.strip().split(',')
    return tuple(map(int, v))


def parse_scanner(lines):
    coordinates = map(parse_coordinates, lines[1:])
    return list(coordinates)


def scanners_iterator(lines):
    current = []
    for line in lines:
        if line:
            current.append(line)
        else:
            yield current
            current = []
    yield current


def parse(lines):
    clean_lines = map(str.strip, lines)
    return list(map(parse_scanner, scanners_iterator(clean_lines)))


def sub(a, b):
    return tuple(ac - bc for ac, bc in zip(a, b))


def get_deltas(scanner, sn, cache):
    if sn not in cache:
        cache[sn] = [
            sub(i, j)
            for i in scanner
            for j in scanner
        ]
    return cache[sn]


def normalize_vector(v):
    return sorted(map(abs, v))


def stringify_v(v):
    return ','.join(map(str, v))


def normalize_deltas(deltas):
    return map(normalize_vector, deltas)


def index_vectors(vectors, keep_zero=True):
    return {stringify_v(v): i for i, v in enumerate(vectors) if keep_zero or any(v)}


def rotate(v, r):
    return tuple(v[ri] * rs for ri, rs in r)


def add(a, b):
    return tuple(ac + bc for ac, bc in zip(a, b))


def transform_v(t, v):
    r, s = t
    return add(s, rotate(v, r))


def transform(t, vectors):
    for v in vectors:
        yield transform_v(t, v)


def compose_transformation(t1, t2):
    rotation1, shift1 = t1
    rotation2, shift2 = t2
    composed_rotation = rotate(rotation1, rotation2)
    composed_shift = add(shift2, rotate(shift1, rotation2))
    return composed_rotation, composed_shift


class Axis:
    def __init__(self, idx, sign):
        self.idx = idx
        self.sign = sign

    def __neg__(self):
        return Axis(self.idx, -self.sign)

    def __repr__(self):
        return '-+'[max(self.sign, 0)] + 'XYZ'[self.idx]

    def __str__(self):
        return 'Axis(%s, %s)' % (self.idx, self.sign)

    def __iter__(self):
        yield self.idx
        yield self.sign

    def __mul__(self, v):
        return Axis(self.idx, self.sign*v)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Axis) and __o.idx == self.idx and __o.sign == self.sign

    def __hash__(self) -> int:
        return hash(repr(self))


X, Y, Z = (Axis(idx, 1) for idx in range(3))

rotate_over_x = (X, -Z, Y)
rotate_over_z = (-Y, X, Z)
rotate_over_y = (-Z, Y, X)
basic_rotations = (X, Y, Z), rotate_over_x, rotate_over_y, rotate_over_z


all_orientations = set(functools.reduce(rotate, rotation_sequence)
                       for rotation_sequence in itertools.combinations_with_replacement(basic_rotations, 4))


def find_candidate_overlaps(a, scanner_a, b, scanner_b, threshold, deltas_cache):
    deltas_a = get_deltas(scanner_a, a, deltas_cache)
    deltas_b = get_deltas(scanner_b, b, deltas_cache)

    indexed_normalized_deltas_a = index_vectors(normalize_deltas(deltas_a), False)
    indexed_normalized_deltas_b = index_vectors(normalize_deltas(deltas_b), False)

    overlapping_norm = set(indexed_normalized_deltas_a.keys()) & set(indexed_normalized_deltas_b.keys())

    dbg('overlapping_norm [%s, %s]' % (a, b), len(overlapping_norm))
    if len(overlapping_norm) < ((threshold-1) * threshold) / 2:
        return False

    candidate_rotations = defaultdict(list)
    candidate_pairs = defaultdict(list)
    for norm_delta_s in overlapping_norm:
        norm_a_idx = indexed_normalized_deltas_a[norm_delta_s]
        norm_b_idx = indexed_normalized_deltas_b[norm_delta_s]
        ai, aj = divmod(norm_a_idx, len(scanner_a))
        bi, bj = divmod(norm_b_idx, len(scanner_b))
        da = sub(scanner_a[ai], scanner_a[aj])
        db = sub(scanner_b[bi], scanner_b[bj])
        for r in all_orientations:
            if da == rotate(db, r):
                candidate_rotations[r].append((da, db))
                candidate_pairs[r].append((ai, bi))
                candidate_pairs[r].append((ai, bj))

    best_rotation = max(candidate_rotations, key=lambda r: len(candidate_rotations[r]))
    dbg('candidate_rotations [%s, %s]' % (a, b), [(k, len(v)) for k, v in candidate_rotations.items()])
    if len(candidate_rotations[best_rotation]) + 1 < 2 * threshold:
        return False

    candidate_shifts = defaultdict(list)
    rotated_b = [rotate(v, best_rotation) for v in scanner_b]

    for ai, bi in candidate_pairs[best_rotation]:
        va = scanner_a[ai]
        vb = rotated_b[bi]
        shift = sub(va, vb)
        candidate_shifts[shift].append((ai, bi))

    dbg(('candidate_shifts [%s, %s]' % (a, b), [(k, len(v)) for k, v in candidate_shifts.items() if len(v) > 1]))

    best_shift = max(candidate_shifts, key=lambda s: len(candidate_shifts[s]))

    dbg('best_shift', best_shift, len(candidate_shifts[best_shift]))

    if len(candidate_shifts[best_shift]) + 1 < 2 * threshold:
        return False

    return best_rotation, best_shift


def join_scanners(scanners, scanner_positions, threshold):
    overlaps = {}
    deltas_cache = {}
    for i, si in enumerate(scanners):
        for j in range(len(scanners)):
            if i != j:
                sj = scanners[j]
                o = find_candidate_overlaps(i, si, j, sj, threshold=threshold, deltas_cache=deltas_cache)
                if o:
                    overlaps[(i, j)] = o

    dbg('overlaps', overlaps)
    transformations = defaultdict(dict)

    remaining_scanners = set(range(len(scanners)))

    while remaining_scanners:
        changed = True
        starting_scanner = next(iter(remaining_scanners))
        remaining_scanners.remove(starting_scanner)
        transformations[starting_scanner][starting_scanner] = ((X, Y, Z), (0, 0, 0))

        while changed:
            changed = False
            for i, j in overlaps:
                dbg(sorted(transformations.keys()))
                if i in transformations[starting_scanner] and j not in transformations[starting_scanner]:
                    ti0 = transformations[starting_scanner][i]
                    tji = overlaps[(i, j)]
                    transformations[starting_scanner][j] = compose_transformation(tji, ti0)
                    remaining_scanners.remove(j)
                    changed = True

    dbg(('transformations', transformations))
    points = defaultdict(set)

    for starting_scanner in transformations:
        for i, t in transformations[starting_scanner].items():
            for p in transform(t, scanners[i]):
                points[starting_scanner].add(p)
            scanner_positions.add(transform_v(t, (0, 0, 0)))

    if len(points) > 1:
        consolidated_scanners = list(map(list, points.values()))
        return join_scanners(consolidated_scanners, scanner_positions, threshold)

    return next(iter(points.values())), scanner_positions


def manhattan(v1, v2):
    return sum(
        abs(i - j) for i, j in zip(v1, v2)
    )


def test_rotation_composition(v):
    for r1 in all_orientations:
        for r2 in all_orientations:
            expected = rotate(rotate(v, r1), r2)
            result = rotate(v, rotate(r1, r2))
            if expected != result:
                print('FAIL:')
                print(' rotate(rotate({r1}, {r2}), {v}) == {result}'.format(r1=r1, r2=r2, v=v, result=result))
                print(' rotate({r2}, rotate({r1}, {v})) == {expected}'.format(r1=r1, r2=r2, v=v, expected=expected))


def test_transform_composition(s1, s2, v):
    for r1 in all_orientations:
        for r2 in all_orientations:
            expected = transform_v((r2, s2), transform_v((r1, s1), v))
            result = transform_v(compose_transformation((r1, s1), (r2, s2)), v)
            if expected != result:
                print('FAIL:')
                print(' transform_v(compose_transformation(({r1},{s1}), ({r2},{s2})), {v}) == {result}'.format(
                    r1=r1, r2=r2, s1=s1, s2=s2, v=v, result=result))
                print(' transform_v(({r2}, {s2}),transform_v(({r1}, {s1}), {v})) == {expected}'.format(
                    r1=r1, r2=r2, s1=s1, s2=s2, v=v, expected=expected))


test_rotation_composition((1, 1, 1))
test_rotation_composition((1, 2, 3))
test_transform_composition((0, 0, 0), (0, 0, 0), (1, 1, 1))
test_transform_composition((0, 0, 0), (0, 0, 0), (1, 2, 3))
test_transform_composition((1, 1, 1), (0, 0, 0), (1, 1, 1))
test_transform_composition((0, 0, 0), (1, 2, 3), (10, 20, 30))
test_transform_composition((1, 2, 3), (40, 50, 60), (700, 800, 900))

if __name__ == '__main__':
    input = sys.stdin.readlines()
    scanners = parse(input)
    points, scanner_positions = join_scanners(scanners, set(), 12)
    print('Part 1:', len(points))
    print('Part 2:', max(manhattan(si, sj) for si, sj in itertools.product(scanner_positions, scanner_positions)))
