import sys

vowels = set('aeiou')
banned = set(map(tuple, ['ab', 'cd', 'pq', 'xy']))

def non_overlapping_repeated_pair(s):
    consecutive_pairs = zip(s, s[1:])
    for idx, pair in enumerate(consecutive_pairs):
        if pair in consecutive_pairs[idx+2:]:
            return True
    return False

def is_nice(s):
    consecutive_triplets = zip(s, s[1:], s[2:])
    return (
        sum(x == z for x, _, z in consecutive_triplets) >= 1 and
        non_overlapping_repeated_pair(s) 
    )

print(sum(is_nice(word) for word in sys.stdin.readlines()))