import sys
from collections import defaultdict, deque

class CommunicationsModule:
    def __init__(self, name, input_names, output_names):
        self._name = name
        self._input_names = input_names
        self._output_names = output_names
        self._high_pulses_sent = 0
        self._low_pulses_sent = 0
        
    def enqueue_pulses(self, is_high, pulse_queue):
        if is_high:
            self._high_pulses_sent += len(self._output_names)
        else:
            self._low_pulses_sent += len(self._output_names)

        for output_name in self._output_names:
            # print(f'{self._name} -{["low", "high"][int(is_high)]}-> {output_name}')
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

class Conjunction(CommunicationsModule):
    def __init__(self, name, input_names, output_names):
        super().__init__(name, input_names, output_names)
        self._memory = {i:False for i in input_names}

    def process_pulse(self, source, is_high, pulse_queue):
        self._memory[source] = is_high
        is_output_high = not all(self._memory.values())
        self.enqueue_pulses(is_output_high, pulse_queue)

class Broadcaster(CommunicationsModule):
    def __init__(self, name, input_names, output_names):
        super().__init__(name, input_names, output_names)

    def process_pulse(self, source, is_high, pulse_queue):
        self.enqueue_pulses(is_high, pulse_queue)

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

def parse(lines):
    inputs = defaultdict(list)

    parsed = [parse_line(line) for line in lines]
    for _, name, output_names in parsed:
        for o in output_names:
            inputs[o].append(name)

    network = {}
    for cls, name, output_names in parsed:
        network[name] = cls(name, inputs[name], output_names)

    return network

def simulate(network):
    BUTTON_PRESSES = 1000
    low_pulses = BUTTON_PRESSES
    for _ in range(BUTTON_PRESSES):
        # print('button -low-> broadcaster')
        pulse_queue = deque()
        network['broadcaster'].process_pulse('button', False, pulse_queue)
        while pulse_queue:
            src, is_high, dst = pulse_queue.popleft()
            dst_module = network.get(dst)
            if dst_module:
                dst_module.process_pulse(src, is_high, pulse_queue)


    low_pulses += sum(x._low_pulses_sent for x in network.values())
    high_pulses = sum(x._high_pulses_sent for x in network.values())
    print(low_pulses, high_pulses)
    return low_pulses * high_pulses

input = sys.stdin
network = parse(input)
print(simulate(network))