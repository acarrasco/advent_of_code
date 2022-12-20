import sys

l = list(enumerate(map(int, sys.stdin)))

already_shifted = set()
i = 0
m = len(l)
while len(already_shifted) != m:
    idx, v = l[i]
    if idx in already_shifted:
        i = (i + 1) % m
    else:
        already_shifted.add(idx)
        del l[i]
        destination = (m - 1 + i + v) % (m-1)
        if destination > i:
            l.insert(destination, (idx, v))
        else:
            l.insert(destination, (idx, v))
            i += 1

values = [v for _, v in l]

zero_idx = values.index(0)

print(sum(values[(i + zero_idx) % m] for i in (1000, 2000, 3000)))