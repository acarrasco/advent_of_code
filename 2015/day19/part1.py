import sys
import itertools
import re
from collections import defaultdict

element_exp = '[A-Z][a-z]?'


def parse_transmutation(line):
    left, *right = re.findall(element_exp, line)
    return left, right


def not_empty(s):
    return s.strip()


def parse(lines):
    line_it = map(str.strip, lines)
    transmutation_lines = itertools.takewhile(not_empty, line_it)
    derivation_rules = defaultdict(list)
    for line in transmutation_lines:
        left, right = parse_transmutation(line)
        derivation_rules[left].append(right)
    target_molecule = re.findall(element_exp, next(line_it))
    return derivation_rules, target_molecule


def derivations(derivation_rules, molecule):
    for i in range(len(molecule)):
        atom = molecule[i]
        for derived in derivation_rules.get(atom, []):
            yield ''.join(molecule[:i] + derived + molecule[i+1:])


table, target = parse(sys.stdin.readlines())
print(len(set(derivations(table, target))))
