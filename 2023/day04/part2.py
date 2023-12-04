import sys
from collections import defaultdict

def parse(line):
    _, numbers = line.split(":")
    winning_numbers, played_numbers = numbers.split("|")
    winning_numbers = set(map(int, winning_numbers.split()))
    played_numbers = set(map(int, played_numbers.split()))
    return winning_numbers, played_numbers

def numbers_matching(winning_numbers, played_numbers):
    matching = len(winning_numbers & played_numbers)
    return matching


def solve(cards):
    multipliers = defaultdict(lambda: 1)
    for i, card in enumerate(cards):
        matching = numbers_matching(*card)
        for j in range(i + 1, i + 1 + matching):
            multipliers[j] += multipliers[i]

    return sum(multipliers[i] for i in range(len(cards)))

print(solve([parse(line) for line in sys.stdin]))