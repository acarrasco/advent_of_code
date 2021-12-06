import sys
from collections import Counter

input = [line.strip() for line in sys.stdin.readlines()]

bits_by_position = zip(*input)
histogram_by_position = [Counter(bits).most_common() for bits in bits_by_position]

gamma, epsilon = zip(*[
    (histogram[0][0], histogram[-1][0])
    for histogram in histogram_by_position])

gamma_decimal = int(''.join(gamma), 2)
epsilon_decimal = int(''.join(epsilon), 2)

print(gamma_decimal * epsilon_decimal)
