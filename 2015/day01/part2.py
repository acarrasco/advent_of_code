import sys
v = {
    '(' : 1,
    ')' : -1,
}

p = 0
floor = 0
for i in sys.stdin.read():
    p += 1
    floor += v.get(i, 0)
    if floor == -1:
        print(p)
        break
