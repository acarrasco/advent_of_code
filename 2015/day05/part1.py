import sys

vowels = set('aeiou')
banned = set(map(tuple, ['ab', 'cd', 'pq', 'xy']))

def is_nice(s):
    consecutive_pairs = zip(s, s[1:])
    return (
        sum(x in vowels for x in s) >= 3 and
        sum(x == y for x, y in consecutive_pairs) >= 1 and
        all((x, y) not in banned for x, y in consecutive_pairs)
    )

print(sum(is_nice(word) for word in sys.stdin.readlines()))