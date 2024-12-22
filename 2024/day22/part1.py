import sys

def parse_line(line):
    return int(line)

def parse(lines):
    return [parse_line(line) for line in lines]

def next_secret(secret):
    '''
    Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
    '''
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))

    return secret

def mix(a, b):
    return a ^ b

def prune(n):
    return n % 16777216

def nth_secret(secret, n):
    for _ in range(n):
        secret = next_secret(secret)
    return secret

def solve(problem):
    return sum(nth_secret(secret, 2000) for secret in problem)

print(solve(parse(sys.stdin)))
