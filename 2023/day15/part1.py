import sys

def parse_line(line):
    return line.split(',')

def parse(lines):
    return parse_line(lines[0].strip())

def my_hash(txt):
    v = 0
    for c in txt:
        v += ord(c)
        v *= 17
        v %= 256
    return v

def solve(problem):
    return sum(map(my_hash, problem))

print(solve(parse(sys.stdin.readlines())))