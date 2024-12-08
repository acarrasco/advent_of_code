import sys
import operator

OPERATORS = [
    operator.add,
    operator.mul,
    lambda a, b: int(str(a) + str(b))
]

def parse_line(line):
    result, operands = line.split(': ')
    return int(result), [int(op) for op in operands.split()]

def parse(lines):
    return [parse_line(line.strip()) for line in lines]

def solve_equation(calibration_value, operands, acc):
    if int(str(acc) + ''.join(map(str, operands))) < calibration_value:
        return 0
    if acc > calibration_value:
        return 0
    if not operands:
        if calibration_value == acc:
            return calibration_value
        else:
            return 0
    next_equations = (solve_equation(calibration_value, operands[1:], acc=op(acc, operands[0])) for op in OPERATORS)
    return next(filter(None, next_equations), 0)

def solve(problem):
    return sum(solve_equation(result, operands[1:], operands[0]) for result, operands in problem)

print(solve(parse(sys.stdin)))
