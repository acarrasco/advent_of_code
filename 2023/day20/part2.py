import sys
from collections import defaultdict, deque
from itertools import count

class CommunicationsModule:
    def __init__(self, name, input_names, output_names):
        self._name = name
        self._input_names = input_names
        self._output_names = output_names
        
    def enqueue_pulses(self, is_high, pulse_queue):
        for output_name in self._output_names:
            pulse_queue.append((self._name, is_high, output_name))


class FlipFlop(CommunicationsModule):
    def __init__(self, name, input_names, output_names):
        super().__init__(name, input_names, output_names)
        self._on = False

    def process_pulse(self, source, is_high, pulse_queue):
        if is_high:
            return
        self._on = not self._on
        self.enqueue_pulses(self._on, pulse_queue)

    def __repr__(self):
        return f'FlipFlop({self._name}, {["off", "on"][int(self._on)]})'

class Conjunction(CommunicationsModule):
    def __init__(self, name, input_names, output_names):
        super().__init__(name, input_names, output_names)
        self._memory = {i:False for i in input_names}

    def process_pulse(self, source, is_high, pulse_queue):
        self._memory[source] = is_high
        is_output_high = not all(self._memory.values())
        self.enqueue_pulses(is_output_high, pulse_queue)

    def __repr__(self):
        memory_str = ', '.join(
           f'{k}={["off", "on"][int(self._memory[k])]}' for k in self._input_names
        )
        return f'Conjunction({self._name}, {memory_str})'


class Broadcaster(CommunicationsModule):
    def __init__(self, name, input_names, output_names):
        super().__init__(name, input_names, output_names)

    def process_pulse(self, source, is_high, pulse_queue):
        self.enqueue_pulses(is_high, pulse_queue)

    def __repr__(self):
        return 'Broadcaster()'

def parse_line(line):
    src, dst = line.strip().split(' -> ')
    if src.startswith('&'):
        src_name = src[1:].strip()
        src_cls = Conjunction
    elif src.startswith('%'):
        src_name = src[1:].strip()
        src_cls = FlipFlop
    else:
        src_name = src.strip()
        src_cls = Broadcaster
    return src_cls, src_name, dst.split(', ')

def update_reachable(node, inputs, explored):
    if node in explored:
        return
    explored.add(node)
    for parent in inputs[node]:
        update_reachable(parent, inputs, explored)

def parse(lines):
    OUTPUT_NODE = 'rx'
    inputs = defaultdict(list)

    parsed = [parse_line(line) for line in lines]
    for _, name, output_names in parsed:
        for o in output_names:
            inputs[o].append(name)

    sub_networks = []
    output_aggregator, = inputs[OUTPUT_NODE]
    aggregator_inputs = inputs[output_aggregator]
    for leaf in aggregator_inputs:
        reachable_nodes = set()
        update_reachable(leaf, inputs, reachable_nodes)
        network = {}
        sub_networks.append(network)
        for cls, name, output_names in parsed:
            if name in reachable_nodes:
                reachable_outputs = [o for o in output_names if o in reachable_nodes]
                network[name] = cls(name, inputs[name], reachable_outputs)

    return sub_networks

def find_cycle(network):
    states_cache = set()
    for i in count():
        s = repr(network)
        if s in states_cache:
            return i - 1 # the cycle was made in the previous iteration
        states_cache.add(s)

        pulse_queue = deque()
        network['broadcaster'].process_pulse('button', False, pulse_queue)
        while pulse_queue:
            src, is_high, dst = pulse_queue.popleft()
            dst_module = network.get(dst)
            if dst_module:
                dst_module.process_pulse(src, is_high, pulse_queue)

def solve(problem):
    networks = problem
    cycles = [find_cycle(n) for n in networks]
    p = 1
    for c in cycles:
        p *= c
    return p

input = sys.stdin
problem = parse(input)
print(solve(problem))