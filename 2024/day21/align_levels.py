import sys

def align(upper, lower):
    sizes = [len(k)+1 for k in lower.split('A')]
    return ''.join(
        s.rjust(k) for
        k,s in zip(sizes, upper)
    )

def align_all(levels):
    prev = levels[0]
    for level in levels[1:]:
        print(prev)
        prev = align(level, prev)
    print(prev)

align_all(sys.stdin.read().splitlines())