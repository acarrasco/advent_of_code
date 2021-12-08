import sys

digits = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg',
]

segments = {
    c: [i for i, s in enumerate(digits) if c in s] for c in 'abcdefg'
}


def parse_line(line):
    all_digits, output = line.strip().split(' | ')
    return map(sorted, all_digits.split()), map(sorted, output.split())


def count_unique_digits(case):
    _all_digits, output = case
    return sum(map(lambda x: len(x) in (2, 3, 4, 7), output))

input = map(parse_line, sys.stdin.readlines())

print(sum(map(count_unique_digits, input)))