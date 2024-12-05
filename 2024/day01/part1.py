import sys

left = []
right = []
for line in sys.stdin:
    a, b = line.split()
    left.append(int(a))
    right.append(int(b))

left.sort()
right.sort()

print(sum(abs(a - b) for a, b in zip(left, right)))
