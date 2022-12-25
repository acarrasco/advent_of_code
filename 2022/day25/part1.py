import sys


def in_base_5(n):
    digits = []
    while n:
        digits.append(n % 5)
        n //= 5
    return digits


ENCODE = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2',
}

DECODE = {s: n for n, s in ENCODE.items()}


def to_snafu(n):
    base_5 = in_base_5(n)
    snafued = []
    carry = 0
    for d in base_5:
        x = d + carry
        if x < 3:
            snafued.append(x)
            carry = 0
        else:
            snafued.append(x - 5)
            carry = 1
    if carry:
        snafued.append(carry)
    return ''.join(ENCODE[w] for w in reversed(snafued))


def from_snafu(snafu):
    n = 0
    for p, d in enumerate(reversed(snafu.strip())):
        n += DECODE[d] * 5**p
    return n


print(to_snafu(sum(map(from_snafu, sys.stdin))))
