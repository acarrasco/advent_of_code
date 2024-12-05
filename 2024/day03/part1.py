import sys
import re

MUL_EXP = r'mul\(([0-9]+),([0-9]+)\)'

def parse(stdin):
    return stdin.read()

def solve(problem):
    matches = re.findall(MUL_EXP, problem)
    return sum(int(a) * int(b) for a, b in matches)

print(solve(parse(sys.stdin)))
