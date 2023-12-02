import sys
import re

textToDigit = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

digitExpression = '|'.join(list(textToDigit.keys()) + list(textToDigit.values()))

def findFirstDigit(line):
    return re.search(digitExpression, line).group(0)

def findLastDigit(line):
    return re.search(digitExpression[::-1], line[::-1]).group(0)[::-1]

def findDigits(line):
    return [findFirstDigit(line), findLastDigit(line)]

def parse(line):
    line = line.strip()
    digits = findDigits(line)
    firstAndLastDigits = textToDigit.get(digits[0], digits[0]) + textToDigit.get(digits[-1], digits[-1])
    return int(firstAndLastDigits)

print(sum(map(parse, sys.stdin)))
