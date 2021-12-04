import sys


def waste_space(s):
    s = s.strip()
    if not s:
        return 0
    sub = 0
    escape = False
    for c in s[1:-1]:
        if escape:
            escape = False
            if c == 'x':
                sub += 2
        elif c == '\\':
            escape = True
            sub += 1
    return 2 + sub


print(sum(waste_space(x) for x in sys.stdin.readlines()))
