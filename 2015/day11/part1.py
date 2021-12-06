import sys

z = ord('z')
a = ord('a')
base = z - a

banned_chars = 'iol'


def next_char(c):
    n = ord(c) + 1
    if n > z:
        return 'a', True
    nc = chr(n)
    if nc in banned_chars:
        return next_char(nc)
    return nc, False


def increase(l, idx):
    nc, carry = next_char(l[idx])
    l[idx] = nc
    return not carry and l or increase(l, idx - 1)


def next_password(s):
    return ''.join(increase(list(s), -1))


def straight_sequence_idx(p):
    triplets = zip(p, p[1:], p[2:])
    for i, (a, b, c) in enumerate(triplets):
        if ord(a)+2 == ord(b) + 1 == ord(c):
            return i
    return -1


def count_repeated_non_overlapping_pairs(p):
    double_letters = set()
    pairs = zip(p, p[1:])
    for a, b in pairs:
        if a == b:
            double_letters.add(a)
    return len(double_letters)


def is_valid_password(p):
    return straight_sequence_idx(p) >= 0 and count_repeated_non_overlapping_pairs(p) >= 2


def password_sequence(start):
    np = start
    while True:
        np = next_password(np)
        yield np


def test_next_password(input, expected):
    res = next_password(input)
    if res != expected:
        raise Exception('Wrong result', input, res, expected)


def test_valid_password(input, expected):
    res = is_valid_password(input)
    if res != expected:
        raise Exception('Wrong result', input, res, expected)


test_valid_password('hijklmmn', False)
test_valid_password('abbceffg', False)
test_valid_password('ghjaabcc', True)
test_valid_password('vzccaabc', True)


test_next_password('a', 'b')
test_next_password('az', 'ba')
test_next_password('ah', 'aj')
test_next_password('azz', 'baa')
test_next_password('ahz', 'aja')


print(next(filter(is_valid_password, password_sequence(sys.stdin.read().strip()))))
