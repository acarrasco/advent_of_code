import sys
from collections import namedtuple
import re

Machine = namedtuple('Machine', ['a', 'b', 'prize'])

BUTTON_EXP = r'X\+([0-9]+), Y\+([0-9]+)'
PRIZE_EXP = r'X=([0-9]+), Y=([0-9]+)'

def parse(lines):
    machines = []
    a = None
    b = None
    prize = None

    for line in lines:
        if line.startswith('Button A'):
            [(x, y)] = re.findall(BUTTON_EXP, line)
            a = int(x), int(y)
        elif line.startswith('Button B'):
            [(x, y)] = re.findall(BUTTON_EXP, line)
            b = int(x), int(y)
        elif line.startswith('Prize'):
            [(x, y)] = re.findall(PRIZE_EXP, line)
            prize = int(x), int(y)
            machines.append(Machine(a, b, prize))

    return machines

def calculate_movements(machine):
    ax, ay = machine.a
    bx, by = machine.b
    px, py = machine.prize

    r = (bx / ax - by / ay)
    if r == 0:
        return 0

    kb = int(0.5 + (px / ax - py / ay) / r)
    ka = int(0.5 + (px / ax - kb * bx / ax))

    if (ka * ax + kb * bx == px
        and ka * ay + kb * by == py
        and ka <= 100
        and kb <= 100):
        return ka * 3 + kb
    return 0

def solve(problem):
    return sum(map(calculate_movements, problem))

print(solve(parse(sys.stdin)))