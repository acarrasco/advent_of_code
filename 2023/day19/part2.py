import sys
from collections import namedtuple

Rule = namedtuple('Rule', 'attribute operator value destination'.split())
Workflow = namedtuple('Workflow', 'name rules default'.split())
PartRanges = namedtuple('PartRanges', list('xmas'))

def parse_rule(txt):
    cond, destination = txt.split(':')
    if '<' in cond:
        attribute, value = cond.split('<')
        operator = '<'
    else:
        attribute, value = cond.split('>')
        operator = '>'
    return Rule(attribute=attribute, operator=operator, value=int(value), destination=destination)

def parse_workflow(line):
    name, rest = line[:-1].split('{')
    rules = rest.split(',')
    default = rules[-1]
    parsed_rules = []
    for rule in rules[:-1]:
        parsed_rule = parse_rule(rule)
        parsed_rules.append(parsed_rule)

    return Workflow(name=name, rules=parsed_rules, default=default)

def parse(txt):
    workflows, _parts = txt.split('\n\n')
    parsed_workflows=[parse_workflow(w.strip()) for w in workflows.split('\n') if w.strip()]
    return parsed_workflows

MAX_RANGE = 4001

def apply_rule(rule, part_ranges):
    attribute = rule.attribute
    rule_value = rule.value
    part_range = getattr(part_ranges, attribute)

    if rule.operator == '<':
        positive_filter = set(range(1, rule_value))
        negative_filter = set(range(rule_value, MAX_RANGE))
    else:
        positive_filter = set(range(rule_value + 1, MAX_RANGE))
        negative_filter = set(range(1, rule_value + 1))

    rule_pass = part_ranges._replace(**{attribute: part_range & positive_filter})
    rule_fail = part_ranges._replace(**{attribute: part_range & negative_filter})

    return (
        (rule.destination, rule_pass),
        rule_fail
    )

def explore_workflows(workflows, workflow, part_ranges):
    if not all(part_ranges):
        return
    elif workflow == 'A':
        yield part_ranges
        return
    elif workflow == 'R':
        return

    w = workflows[workflow]
    next_part_ranges = part_ranges
    for rule in w.rules:
        (rule_pass_dest, rule_pass_range), rule_fail_range = apply_rule(rule, next_part_ranges)
        yield from explore_workflows(workflows, rule_pass_dest, rule_pass_range)
        next_part_ranges = rule_fail_range

    yield from explore_workflows(workflows, w.default, next_part_ranges)

def part_ranges_combinations(part_ranges):
    p = 1
    for r in part_ranges:
        p *= len(r)
    return p

def solve(problem):
    indexed_workflows = {
        w.name: w for w in problem
    }
    initial_ranges = PartRanges(
        x=set(range(1, MAX_RANGE)),
        m=set(range(1, MAX_RANGE)),
        a=set(range(1, MAX_RANGE)),
        s=set(range(1, MAX_RANGE)),
    )
    accepted_ranges = explore_workflows(indexed_workflows, 'in', initial_ranges)    
    return sum(part_ranges_combinations(pr) for pr in accepted_ranges)

input = sys.stdin.read()
problem = parse(input)
print(solve(problem))