import sys

W = 3
numbers = [int(line.strip()) for line in sys.stdin.readlines()]

print(sum(
    sum(numbers[i:i+W]) < sum(numbers[i+1:i+1+W])
    for i in range(len(numbers))
))
