import sys

actions_mapping = {
    'forward': [('x', 1), ('y', 1, 'aim')],
    'backward': [('x', -1), ('y', -1, 'aim')],
    'up': [('aim', -1)],
    'down': [('aim', 1)]
}

actions_and_magnitudes = (line.strip().split() for line in sys.stdin.readlines())

state = {
    'x': 0,
    'y': 0,
    'aim': 0,
}

def mult(factors):
    m = 1
    for i in factors:
        m *= state.get(i, i)
    return m

for action, magnitude in actions_and_magnitudes:
    magnitude = int(magnitude)
    for target, *factors in actions_mapping[action]:
        state[target] += magnitude * mult(factors)

print(state['x'] * state['y'])
