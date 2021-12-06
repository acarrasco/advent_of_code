import sys
import json

def sum_numbers(o):
    if isinstance(o, int):
        return o
    elif isinstance(o, list):
        return sum(map(sum_numbers, o))
    elif isinstance(o, dict):
        return sum(map(sum_numbers, o.values()))
    else:
        return 0

print(sum_numbers(json.load(sys.stdin)))