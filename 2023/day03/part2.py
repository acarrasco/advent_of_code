import sys
from collections import namedtuple

NumberLocation = namedtuple("NumberLocation", ["number", "row", "start", "end"])

def parse(lines):
    grid = []
    for line in lines:
        grid.append(line.strip())
    return grid

def findAllNumberLocations(grid):
    numbers = []
    currentNumber = ""
    start = 0

    for i, row in enumerate(grid):
        if currentNumber:
            numbers.append(NumberLocation(int(currentNumber), i-1, start, len(row) - 1))
        currentNumber = ""
        start = 0
        for j, cell in enumerate(row):
            if cell.isdigit():
                if not currentNumber:
                    start = j
                currentNumber += cell
            elif currentNumber:
                numbers.append(NumberLocation(int(currentNumber), i, start, j - 1))
                currentNumber = ""

    return numbers

def findAdjacentNumbers(numberLocations, i, j):
    numbers = []
    for number, row, start, end in numberLocations:
        if i-1 <= row <= i+1 and start-1 <= j <= end+1:
            numbers.append(number)
    return numbers

def findGearRatios(grid):
    gearRatios = []
    numberLocations = findAllNumberLocations(grid)
    for i, row in enumerate(grid):        
        for j, cell in enumerate(row):
            if cell == "*":
                adjacent = findAdjacentNumbers(numberLocations, i, j)
                if len(adjacent) == 2:
                    gearRatios.append(adjacent[0] * adjacent[1])

    return gearRatios

def main():
    grid = parse(sys.stdin)
    print(sum(findGearRatios(grid)))

if __name__ == "__main__":
    main()