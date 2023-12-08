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

def steps_in_exit_for_state(instructions, graph, starting_state):
    step = 0
    
    steps = []
    visited_states = set()
    state = starting_state

    for instruction in itertools.cycle(instructions):
        step += 1
        state = graph[state, instruction]
        if state.endswith('Z'):
            steps.append(step)

        # If we have already visited this state at this instruction, we are in a loop
        if (state, step % len(instructions)) in visited_states:
            return steps
        visited_states.add((state, step % len(instructions)))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mcm(numbers):
    lcm = 1
    for number in numbers:
        lcm = lcm * number // gcd(lcm, number)
    return lcm
        
def solve(instructions, graph):
    states = [state for (state, _) in graph if state.endswith('A')]
    steps = [steps_in_exit_for_state(instructions, graph, state) for state in states]
    for step in steps:
        if len(step) != 1:
            raise Exception("I cannot handle this input")
    return mcm(s[0] for s in steps)
        
print(solve(*parse_problem(sys.stdin.readlines())))