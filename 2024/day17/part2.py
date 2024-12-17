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


def dbg_combo_operand(operand):
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
        return 'A'
    elif operand == 5:
        return 'B'
    elif operand == 6:
        return 'C'
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

def disassemble(instructions):
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
    ip = 0
    while ip < len(instructions):
        opcode = instructions[ip]
        ip += 1
        operand = instructions[ip]
        ip += 1

        if opcode == 0:
            print(f'adv: A = A // 2**{dbg_combo_operand(operand)}')
        elif opcode == 1:
            print(f'bxl: B = B ^ {operand}')
        elif opcode == 2:
            print(f'bst: B = {dbg_combo_operand(operand)} % 8')
        elif opcode == 3:
            print(f'jnz: if A then IP = {operand}')
        elif opcode == 4:
            print(f'bxc: B = B ^ C')
        elif opcode == 5:
            print(f'out: {dbg_combo_operand(operand)} % 8')
        elif opcode == 6:
            print(f'bdv: B = A // 2**{dbg_combo_operand(operand)}')
        elif opcode == 7:
            print(f'cdv: C = A // 2**{dbg_combo_operand(operand)}')
        else:
            raise Exception('Invalid opcode', opcode)
    return True

def run_program(registers, instructions):
    out = []
    while execute(registers, instructions, out):
        pass
    return out

def shared_prefix(expected, out):
    for i, (e, o) in enumerate(zip(expected, out)):
        if e != o:
            return i
    return i

def solve(problem):
    original_registers, instructions = problem
    a = 0
    out = None
    base = 1
    while out != instructions:
        a += base
        registers = {}
        registers.update(original_registers, A=a)
        out = run_program(registers, instructions)
        p = shared_prefix(instructions, out)
        if p and p % 3 == 0:
            # print((oct(a), ','.join(map(str, out)), base))
            base = 1 << (1 + 3 * p)
    return a

print(solve(parse(sys.stdin)))
