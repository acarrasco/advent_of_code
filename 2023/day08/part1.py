import itertools
import sys

def parse_graph(lines):
    graph = {}

    for line in lines:
        src, dst = line.split(" = ")
        left, right = dst.strip()[1:-1].split(", ")
        graph[src, 'L'] = left
        graph[src, 'R'] = right
    
    return graph

def parse_problem(lines):
    instructions = lines[0].strip()

    return instructions, parse_graph(lines[2:])

def solve(instructions, graph):
    state = 'AAA'
    cursor = 0
    tape = set()

    steps = 0
    for instruction in itertools.cycle(instructions):
        steps += 1
        state = graph[state, instruction]
        if state == 'ZZZ':
            return steps
        
print(solve(*parse_problem(sys.stdin.readlines())))