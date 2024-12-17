import sys

REGISTER_PREFIX = 'Register '
PROGRAM_PREFIX = 'Program'
IP = 'IP'

def parse(lines):
    registers = {}
    program = None
    for line in lines:
        if line.startswith(REGISTER_PREFIX):
            register = line[len(REGISTER_PREFIX)]
            registers[register] = int(line.split()[-1])
        elif line.startswith(PROGRAM_PREFIX):
            program_values = line.split()[-1]
            program = [int(x) for x in program_values.split(',')]
    registers[IP] = 0
    return registers, program

def combo_operand(registers, operand):
    '''
    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.
    '''

    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']
    else:
        raise Exception('Invalid combo operand', operand)

def execute(registers, instructions, out):
    '''
The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)
    '''
    if registers[IP] >= len(instructions) - 1:
        return False
    
    opcode = instructions[registers[IP]]
    registers[IP] += 1
    operand = instructions[registers[IP]]
    registers[IP] += 1

    if opcode == 0:
        numerator = registers['A']
        denominator = 2 ** combo_operand(registers, operand)
        result = numerator // denominator
        registers['A'] = result
    elif opcode == 1:
        result = registers['B'] ^ operand
        registers['B'] = result
    elif opcode == 2:
        result = combo_operand(registers, operand) % 8
        registers['B'] = result
    elif opcode == 3:
        if registers['A']:
            registers[IP] = operand
    elif opcode == 4:
        result = registers['B'] ^ registers['C']
        registers['B'] = result
    elif opcode == 5:
        result = combo_operand(registers, operand) % 8
        out.append(result)
    elif opcode == 6:
        numerator = registers['A']
        denominator = 2 ** combo_operand(registers, operand)
        result = numerator // denominator
        registers['B'] = result
    elif opcode == 7:
        numerator = registers['A']
        denominator = 2 ** combo_operand(registers, operand)
        result = numerator // denominator
        registers['C'] = result
    else:
        raise Exception('Invalid opcode', opcode)
    return True

def solve(problem):
    registers, instructions = problem
    out = []
    while execute(registers, instructions, out):
        pass
    return ','.join(map(str, out))

print(solve(parse(sys.stdin)))
