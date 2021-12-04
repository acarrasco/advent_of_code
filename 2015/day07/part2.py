import sys

bitmask = (1 << 17) - 1

def build_circuit(lines):
    circuit = {}
    for line in lines:
        input, output = line.split(' -> ')
        circuit[output.strip()] = input.strip()
    return circuit

def eval_circuit(circuit, input):
    if isinstance(input, int):
        return input
    elif input.isdigit():
        output = int(input)
    elif input.isalpha():
        output = eval_circuit(circuit, circuit[input])
        circuit[input] = output
    else:    
        args = input.split()
        if args[0] == 'NOT':
            output = eval_circuit(circuit, args[1]) ^ bitmask
        elif args[1] == 'AND':
            output = eval_circuit(circuit, args[0]) & eval_circuit(circuit, args[2])
        elif args[1] == 'OR':
            output = eval_circuit(circuit, args[0]) | eval_circuit(circuit, args[2])
        elif args[1] == 'LSHIFT':
            output = bitmask & (eval_circuit(circuit, args[0]) << eval_circuit(circuit, args[2]))
        elif args[1] == 'RSHIFT':
            output = eval_circuit(circuit, args[0]) >> eval_circuit(circuit, args[2])
        else:
            raise Exception('Invalid input', input)
    
    #print('%s = %s' % (input, output))
    return output

circuit = build_circuit(sys.stdin.readlines())
circuit['b'] = 3176

print(eval_circuit(circuit, 'a'))