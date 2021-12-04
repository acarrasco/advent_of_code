import sys


def extra_memory(s):
    s = s.strip()
    if not s:
        return 0
    extra = 0
    for c in s[1:-1]:
        if c == '\\':
            extra += 1
        elif c == '"':
            extra += 1
    return 4 + extra


def test(s, expected):
    res = extra_memory(s)
    if res != expected:
        raise Exception('Wrong result', s, expected, res)


test(r'""', 4)
test(r'"abc"', 4)
test(r"aaa\"aaa", 6)
test(r'"\x27', 5)

print(sum(extra_memory(x) for x in sys.stdin.readlines()))
