import sys
import re

INS_EXP = r"mul\(([0-9]+),([0-9]+)\)|(do)\(\)|(don't)\(\)"

def parse(stdin):
    return stdin.read()

def solve(problem):
    matches = re.findall(INS_EXP, problem)
    s = 0
    enabled = True
    for a, b, do, dont in matches:
        if do:
            enabled = True
        elif dont:
            enabled = False
        if enabled and a and b:
            s += int(a) * int(b)
    return s

print(solve(parse(sys.stdin)))
