import sys
import re


def highest_hitting_trayectory(area):
    _, (y0, _) = area
    return y0*(y0+1)/2


def parse_area(text):
    exp = r'target area: x=([0-9]+)..([0-9]+), y=(-[0-9]+)..(-[0-9]+)'
    m = re.match(exp, text)
    x0, x1, y0, y1 = (int(i) for i in m.groups())
    return (x0, x1), (y0, y1)


test_area = (20, 30), (-10, -5)

print(highest_hitting_trayectory(parse_area(sys.stdin.read())))
