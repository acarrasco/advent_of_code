import sys
import part1

wires = part1.parse(sys.stdin)

print('digraph {')
for w in wires:
    if w.op == 'CONSTANT':
        pass
    else:
        a, b = w.inputs
        c = w.name
        if c[0] == 'z':
            color = ' style=filled fillcolor=coral'
        else:
            color = ''
        print(f'{c} [label="{c} = {w.op}({a}, {b})" shape=rectangle {color}]')
        print(f'{a} -> {c}')
        print(f'{b} -> {c}')

print('}')