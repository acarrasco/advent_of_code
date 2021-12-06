import sys
import re
import itertools

action_factor = {
    'gain': 1,
    'lose': -1,
}


def parse_input(lines):
    line_exp = '([a-zA-Z]+) would ((?:gain)|(?:lose)) ([0-9]+) happiness units by sitting next to ([a-zA-Z]+).'
    happiness_change = {}
    people = set()
    for line in lines:
        person_a, action, amount, person_b = re.match(line_exp, line).groups()
        happiness_change[person_a, person_b] = action_factor[action] * int(amount)
        people.add(person_a)
        people.add(person_b)
    return happiness_change, list(people)


def calculate_happines(change, perm):
    s = 0
    n = len(perm)
    for i in range(n):
        a, b, c = perm[i - 1], perm[i], perm[(i + 1) % n]
        s += change.get((b, a), 0)
        s += change.get((b, c), 0)
    return s


def solve(change, people):
    return max(calculate_happines(change, ('me',) + perm)
               for perm in itertools.permutations(people))


print(solve(*parse_input(sys.stdin.readlines())))
