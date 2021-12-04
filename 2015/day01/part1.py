import sys
v = {
    '(' : 1,
    ')' : -1,
}

print(sum(v.get(x, 0) for x in sys.stdin.read()))