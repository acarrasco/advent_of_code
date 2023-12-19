import sys
from collections import namedtuple
from operator import __ge__, __le__

Part = namedtuple('Part', list('xmas'))
Rule = namedtuple('Rule', 'attribute operator value destination'.split())
Workflow = namedtuple('Workflow', 'name rules default'.split())
Problem = namedtuple('Problem', 'workflows parts'.split())

def parse_part(line):
    without_braces = line[1:-1]
    tokens = without_braces.split(',')
    attrs = {}
    for token in tokens:
        name, value = token.split('=')
        attrs[name] = int(value)
    return Part(**attrs)

def parse_rule(txt):
    cond, destination = txt.split(':')
    if '<' in cond:
        attribute, value = cond.split('<')
        operator = __le__
    else:
        attribute, value = cond.split('>')
        operator = __ge__
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
    workflows, parts = txt.split('\n\n')
    parsed_workflows=[parse_workflow(w.strip()) for w in workflows.split('\n') if w.strip()]
    parsed_parts = [parse_part(p.strip()) for p in parts.split('\n') if p.strip()]
    return Problem(workflows=parsed_workflows, parts=parsed_parts)

def rule_destination(rule, part):
    attribute = rule.attribute
    rule_value = rule.value
    part_value = getattr(part, attribute)
    if rule.operator(part_value, rule_value):
        return rule.destination
    return None

def execute_workflow(workflows, workflow, part):
    if workflow == 'A' or workflow == 'R':
        return workflow
    w = workflows[workflow]
    for rule in w.rules:
        dest = rule_destination(rule, part)
        if dest:
            return execute_workflow(workflows, dest, part)
    return execute_workflow(workflows, w.default, part)

def solve(problem):
    indexed_workflows = {
        w.name: w for w in problem.workflows
    }

    results = (
        (part, execute_workflow(indexed_workflows, 'in', part)) for part in problem.parts
    )

    acc = 0
    for part, dest in results:
        if dest == 'A':
            acc += part.x + part.m + part.a + part.s
    return acc

input = sys.stdin.read()
problem = parse(input)
print(solve(problem))