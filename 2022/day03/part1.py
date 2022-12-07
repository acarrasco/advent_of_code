import sys


def priority(item):
    n = ord(item)
    if 65 <= n <= 90:
        return n - 38
    elif 97 <= n <= 122:
        return n - 96 
    else:
        raise ('Invalid item', item)

def find_repeated(rucksack):
    rucksack_size = len(rucksack)
    compartment_size = rucksack_size // 2
    first_compartment = rucksack[:compartment_size]
    second_compartment = rucksack[compartment_size:]
    return set(first_compartment) & set(second_compartment)

rucksacks = map(str.strip, sys.stdin.readlines())
repated_elements = list(map(find_repeated, rucksacks))
priorities = [priority(*item) for item in repated_elements]
print(sum(priorities))