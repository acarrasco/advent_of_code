import sys

left = []
right = []
for line in sys.stdin:
    a, b = line.split()
    left.append(int(a))
    right.append(int(b))

left = set(left)

print(sum(x for x in right if x in left))
