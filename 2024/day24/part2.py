import sys
from collections import namedtuple, deque
from itertools import combinations

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
    if ':' in line:
        name, _value = line.split(':')
        return Wire(name, (None, None), None)

def parse(lines):
    return list(filter(None, map(parse_line, lines)))

def wire_value(wires, inputs, name, swaps, checking=None):
    if checking is None:
        checking = set()

    name = swaps.get(name, name)

    if name in checking:
        return -1 # infinite loop

    if name[0] in 'xy' and name not in inputs:
        inputs[name] = 0

    if name not in inputs:
        (a, b), op = wires[name]
        checking.add(name)
        inputs[name] = OPS[op](
            wire_value(wires, inputs, a, swaps, checking),
            wire_value(wires, inputs, b, swaps, checking)
        )
    return inputs[name]

def test_wire(wires, name, swaps):
    idx = int(name[1:])
    for x in range(4):
        for y in range(4):
            inputs = {}
            x0 = f'x{idx:02}'
            x_1 = f'x{idx-1:02}'
            y0 = f'y{idx:02}'
            y_1 = f'y{idx-1:02}'
            
            if x0 not in wires and x >> 1:
                break
            if x_1 not in wires and x & 1:
                break
            if y0 not in wires and y >> 1:
                break
            if y_1 not in wires and y & 1:
                break

            inputs[x0] = x >> 1
            inputs[y0] = y >> 1
            inputs[x_1] = x & 1
            inputs[y_1] = y & 1
            expected = ((x + y) >> 1) & 1
            v = wire_value(wires, inputs, name, swaps)
            if expected != v:
                return False
    return True

def get_swap_candidates(wires, name):
    q = deque()
    seen = {name}
    candidates = [name]
    idx = int(name[1:])
    q.append(f'z{idx+1:02}')
    q.append(name)
    while q:
        w = q.popleft()
        if w[0] not in 'xy':
            if w in wires:
                (a, b), _ = wires[w]
                q.append(a)
                q.append(b)
            if w[0] != 'z' and w not in seen:
                seen.add(w)
                candidates.append(w)
    return candidates

def pairs_by_depth(seq):
    n = len(seq)
    for s in range(1, 2 * n - 2):
        for a in range(max(0, 1 + s - n), (s+1) // 2):
            yield seq[a], seq[s - a]

def solve(problem):
    wires = { w.name: (w.operands, w.op) for w in problem }
    swaps = {}

    for i in range(0, 46):
        name = f'z{i:02}'
        if not test_wire(wires, name, swaps):
            for a, b in pairs_by_depth(get_swap_candidates(wires, name)):
                candidate_swaps = {a: b, b: a}
                candidate_swaps.update(swaps)
                if test_wire(wires, name, candidate_swaps):
                    swaps = candidate_swaps
                    print('swap', a, b)
                    break
    
    for i in range(0, 46):
        name = f'z{i:02}'
        if not test_wire(wires, name, swaps):
            print('bad wire', name)

    return ','.join(sorted(swaps))

if __name__ == '__main__':
    print(solve(parse(sys.stdin)))
