import sys
import collections

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
    secret = (((secret * 64) ^ secret)) % 16777216
    secret = (((secret // 32) ^ secret)) % 16777216
    secret = (((secret * 2048) ^ secret)) % 16777216

    return secret

def generate_price_sequence(secret, n):
    for _ in range(n):
        yield secret % 10
        secret = next_secret(secret)

def generate_diffs_and_price(prices):
    it = iter(prices)
    a = next(it, None)
    b = next(it, None)
    c = next(it, None)
    d = next(it, None)
    e = next(it, None)

    while e is not None:
        yield (b-a, c-b, d-c, e-d), e
        a, b, c, d = b, c, d, e
        e = next(it, None)

def first_diff_to_price(seq_and_price):
    prices = {}
    for seq, price in seq_and_price:
        if seq not in prices:
            prices[seq] = price
    return prices

def solve(problem):
    diffs_to_total_prices = collections.defaultdict(int)

    for secret in problem:
        prices = generate_price_sequence(secret, 2001)
        diffs_and_prices = generate_diffs_and_price(prices)
        for diff, price in first_diff_to_price(diffs_and_prices).items():
            diffs_to_total_prices[diff] += price

    return max(diffs_to_total_prices.values())

print(solve(parse(sys.stdin)))
