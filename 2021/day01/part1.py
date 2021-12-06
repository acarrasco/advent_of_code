import sys

numbers = [int(line.strip()) for line in sys.stdin.readlines()]
print(sum(x < y for (x, y) in zip(numbers, numbers[1:])))
