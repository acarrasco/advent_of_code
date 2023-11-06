import sys
import re
from collections import namedtuple

State = namedtuple('State', ['a', 'b', 'ic'])

def parse_line(line):
    tokens = re.split('[ ,]+', line.strip())
    if len(tokens) == 3:
        return tokens[0], tokens[1], int(tokens[2])
    elif tokens[0] == 'jmp':
        return tokens[0], int(tokens[1])
    else:
        return tuple(tokens)

def parse(lines):
    return list(map(parse_line, lines))

def execute(program, state: State):
    instruction = program[state.ic]
    
    match instruction:
        case 'hlf', 'a':
            return State(state.a // 2, state.b, state.ic + 1)
        case 'hlf', 'b':
            return State(state.a, state.b // 2, state.ic + 1)

        case 'tpl', 'a':
            return State(state.a * 3, state.b, state.ic + 1)
        case 'tpl', 'b':
            return State(state.a, state.b * 3, state.ic + 1)

        case 'inc', 'a':
            return State(state.a + 1, state.b, state.ic + 1)
        case 'inc', 'b':
            return State(state.a, state.b + 1, state.ic + 1)
        
        case 'jmp', offset:
            return State(state.a, state.b, state.ic + offset)
        
        case 'jie', 'a', offset:
            if state.a % 2 == 0:
                return State(state.a, state.b, state.ic + offset)
        case 'jie', 'b', offset:
            if state.b % 2 == 0:
                return State(state.a, state.b, state.ic + offset)

        case 'jio', 'a', offset:
            if state.a == 1:
                return State(state.a, state.b, state.ic + offset)
        case 'jio', 'b', offset:
            if state.b == 1:
                return State(state.a, state.b, state.ic + offset)

    return State(state.a, state.b, state.ic + 1)

def solve(program):
    size = len(program)
    state = State(1, 0, 0)
    while state.ic < size:
        state = execute(program, state)
    return state.b

program = parse(sys.stdin)
print(solve(program))