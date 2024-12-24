import sys
from collections import namedtuple
from functools import cache

Wire = namedtuple('Wire', ['name', 'inputs', 'op'])

OPS = {
    'AND': lambda a, b: a & b,
    'XOR': lambda a, b: a ^ b,
    'OR': lambda a, b: a | b,
}

def parse_line(line):
    if '->' in line:
        inputs, name = line.split(' -> ')
        a, op, b = inputs.split()
        return Wire(name, (a, b), op)
    elif ':' in line:
        name, value = line.split(': ')
        return Wire(name, (int(value),), 'CONSTANT')

def parse(lines):
    return [parse_line(line.strip()) for line in lines if line.strip()]

def solve(problem):
    wires = { w.name: (w.inputs, w.op) for w in problem }
    z_names = sorted(w.name for w in problem if w.name.startswith('z'))

    @cache
    def wire_value(name):
        inputs, op = wires[name]
        if op == 'CONSTANT':
            value, = inputs
            return value
        else:
            a, b = inputs
            return OPS[op](
                wire_value(a),
                wire_value(b)
            )

    z_values = [wire_value(name) for name in z_names]

    return int(''.join(map(str, z_values[::-1])), base=2)


if __name__ == '__main__':
    print(solve(parse(sys.stdin)))
