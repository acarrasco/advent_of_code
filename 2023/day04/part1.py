import sys


def parse(line):
    _, numbers = line.split(":")
    winning_numbers, played_numbers = numbers.split("|")
    winning_numbers = set(map(int, winning_numbers.split()))
    played_numbers = set(map(int, played_numbers.split()))
    return winning_numbers, played_numbers

def card_points(winning_numbers, played_numbers):
    matching = len(winning_numbers & played_numbers)
    return matching and 2**(matching - 1)


print(sum(card_points(*parse(line)) for line in sys.stdin))