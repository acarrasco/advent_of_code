import sys
from collections import namedtuple
from functools import cache

Wire = namedtuple('Wire', ['name', 'operands', 'op'])

OPS = {
    'AND': lambda a, b: a & b,
    'XOR': lambda a, b: a ^ b,
    'OR': lambda a, b: a | b,
}

def parse_line(line):
    if '->' in line:
        operands, name = line.split(' -> ')
        a, op, b = operands.split()
        return Wire(name.strip(), (a, b), op)

def parse(lines):
    return list(filter(None, map(parse_line, lines)))

def wire_value(wires, inputs, name):
    if name[0] in 'xy' and name not in inputs:
        inputs[name] = 0

    if name not in inputs:
        (a, b), op = wires[name]
        inputs[name] = OPS[op](
            wire_value(wires, inputs, a),
            wire_value(wires, inputs, b)
        )
    return inputs[name]

def test_wire(wires, name):
    idx = int(name[1:])
    for x in range(4):
        for y in range(4):
            inputs = {}
            inputs[f'x{idx:02}'] = x >> 1
            inputs[f'y{idx:02}'] = y >> 1
            inputs[f'x{idx-1:02}'] = x & 1
            inputs[f'y{idx-1:02}'] = y & 1
            expected = ((x + y) >> 1) & 1
            v = wire_value(wires, inputs, name)
            # print(inputs, expected, v)
            if expected != v:
                return False
    return True


def solve(problem):
    wires = { w.name: (w.operands, w.op) for w in problem }

    for i in range(1, 45):
        if not test_wire(wires, f'z{i:02}'):
            print(i)
    return

if __name__ == '__main__':
    print(solve(parse(sys.stdin)))
