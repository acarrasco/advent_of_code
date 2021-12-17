import sys
import re
from collections import defaultdict

def moments_vx_hits(area):
    (x0, x1), (y0, y1) = area
    for vx in range(1, x1+1):
        currentvx = vx
        x = 0
        for t in range(2*abs(y0)):
            x += currentvx
            currentvx = max(0, currentvx -1)
            if x0 <= x <= x1:
                yield t, vx


def moments_vy_hits(area):
    (x0, x1), (y0, y1) = area
    for vy in range(-2*abs(y0-1), 2*abs(y1)+1):
        cvy = vy
        y = 0
        for t in range(2*abs(y0)):
            y += cvy
            cvy -= 1
            if y0 <= y <= y1:
                yield t, vy



def count_hits(area):
    tx = defaultdict(set)
    ty = defaultdict(set)

    for t, vx in moments_vx_hits(area):
        tx[t].add(vx)
    for t, vy in moments_vy_hits(area):
        ty[t].add(vy)

    hits = set()
    for t in ty:
        for vx in tx[t]:
            for vy in ty[t]:
                hits.add((vx, vy))
    return len(hits)

def parse_area(text):
    exp = r'target area: x=([0-9]+)..([0-9]+), y=(-[0-9]+)..(-[0-9]+)'
    m = re.match(exp, text)
    x0, x1, y0, y1 = (int(i) for i in m.groups())
    return (x0, x1), (y0, y1)


print(count_hits(parse_area(sys.stdin.read())))
