import sys
from collections import namedtuple, defaultdict

Point = namedtuple('Point', list('xyz'))

class Brick:
    def __init__(self, idx, a, b):
        self.idx = idx
        self.a = a
        self.b = b
        assert all(ai <= bi for ai, bi in zip(a, b))

    def __repr__(self):
        return f'Brick({self.idx}, {self.a}, {self.b})'

    def drop_one(self):
        ax, ay, az = self.a
        bx, by, bz = self.b
        return Brick(self.idx, Point(ax, ay, az-1), Point(bx, by, bz-1))

class Volume:
    def __init__(self):
        self.coordinates = {}
        self.bricks = {}
        self.supporting = defaultdict(set)
        self.supported_by = defaultdict(set)

    def _insert_brick(self, brick):
        for x in range(brick.a.x, brick.b.x + 1):
            for y in range(brick.a.y, brick.b.y + 1):
                for z in range(brick.a.z, brick.b.z + 1):
                    self.coordinates[x, y, z] = brick.idx
        self.bricks[brick.idx] = brick

    def _supported_by(self, brick):
        z = brick.a.z - 1

        if z == 0:
            # -1 is the floor
            return (-1,)

        supporting_bricks = set()
        for x in range(brick.a.x, brick.b.x + 1):
            for y in range(brick.a.y, brick.b.y + 1):
                if (x, y, z) in self.coordinates:
                    supporting_bricks.add(self.coordinates[x, y, z])
        return supporting_bricks

    def drop_brick(self, brick):
        supporting = ()
        dropped_brick = brick
        while not(supporting := self._supported_by(dropped_brick)):
            dropped_brick = dropped_brick.drop_one()

        self._insert_brick(dropped_brick)
        for s in supporting:
            self.supporting[s].add(brick.idx)
            self.supported_by[brick.idx].add(s)

def parse_line(n, line):
    a, b = line.split('~')
    pa = [int(n) for n in a.split(',')]
    pb = [int(n) for n in b.split(',')]
    return Brick(n, Point(*pa), Point(*pb))

def parse(lines):
    return [parse_line(i, line.strip()) for i, line in enumerate(lines) if line.strip()]

def update_falling(brick, supporting, supported_by, fallen):
    for sb in supporting[brick]:
        if not (supported_by[sb] - fallen):
            fallen.add(sb)
            update_falling(sb, supporting, supported_by, fallen)

def solve(bricks):
    volume = Volume()
    sorted_bricks = sorted(bricks, key=lambda b:b.a.z)
    for brick in sorted_bricks:
        volume.drop_brick(brick)

    total = 0
    for b in bricks:
        fallen = {b.idx}
        update_falling(b.idx, volume.supporting, volume.supported_by, fallen)
        total += len(fallen) - 1

    return total

print(solve(parse(sys.stdin.readlines())))