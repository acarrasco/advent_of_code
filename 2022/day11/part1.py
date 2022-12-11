import sys
import heapq
from dataclasses import dataclass
from typing import Callable, List

@dataclass
class Monkey:
    items: List[int]
    operation: Callable[[int], int]
    test: int
    if_true: int
    if_false: int

monkeys = [
    Monkey([59, 65, 86, 56, 74, 57, 56], lambda x: x * 17, 3, 3,6),
    Monkey([63, 83, 50, 63, 56], lambda x: x + 2, 13, 3, 0),
    Monkey([93, 79, 74, 55], lambda x: x + 1, 2, 0, 1),
    Monkey([86, 61, 67, 88, 94, 69, 56, 91], lambda x: x + 7, 11, 6, 7),
    Monkey([76, 50, 51], lambda x: x * x, 19, 2, 5),
    Monkey([77, 76], lambda x: x + 8, 17, 2, 1),
    Monkey([74], lambda x: x * 2, 5, 4, 7),
    Monkey([86, 85, 52, 86, 91, 95], lambda x: x + 6, 7, 4, 5),
]

# monkeys = [
#     Monkey([79, 98], lambda x: x * 19, 23, 2, 3),
#     Monkey([54, 65, 75, 74], lambda x: x + 6, 19, 2, 0),
#     Monkey([79, 60, 97], lambda x: x * x, 13, 1, 3),
#     Monkey([74], lambda x: x + 3, 17, 0, 1),
# ]


times_inspected = [0 for _ in monkeys]

def simulate_turn(monkey_index):
    monkey = monkeys[monkey_index]
    while monkey.items:
        times_inspected[monkey_index] += 1
        item = monkey.items.pop()
        new_item = monkey.operation(item) // 3
        if new_item % monkey.test == 0:
            new_monkey_index = monkey.if_true
        else:
            new_monkey_index = monkey.if_false
        monkeys[new_monkey_index].items.append(new_item)


def simulate_round():
    for monkey_index in range(len(monkeys)):
        simulate_turn(monkey_index)

def solve(rounds):
    for _ in range(rounds):
        simulate_round()
    a, b = heapq.nlargest(2, times_inspected)
    return a * b

print(solve(20))