import sys
def parse(line):
    lineWithoutAlpha = ''.join([c for c in line if c.isdigit()])
    return int(lineWithoutAlpha[0] + lineWithoutAlpha[-1])
print(sum(map(parse, sys.stdin)))