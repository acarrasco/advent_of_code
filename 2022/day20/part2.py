import sys

l = list(enumerate(int(v) * 811589153 for v in sys.stdin))
m = len(l)
original = l[::]
i = 0
for r in range(10):
    for idx, v in original:
        i = l.index((idx, v))
        del l[i]
        destination = (m - 1 + i + v) % (m - 1)
        if destination > i:
            l.insert(destination, (idx, v))
        else:
            l.insert(destination, (idx, v))
            i = (i + 1) % m

values = [v for _, v in l]
zero_idx = values.index(0)

print(sum(values[(i + zero_idx) % m] for i in (1000, 2000, 3000)))