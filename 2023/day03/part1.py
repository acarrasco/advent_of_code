import sys

NEIGHBOURS_DELTAS = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]


def parse(lines):
    grid = []
    for line in lines:
        grid.append(list(line.strip()))

    return grid

def findPartNumbers(grid):
    partNumbers = []

    currentNumber = ""
    isPartNumber = False

    for i, row in enumerate(grid):
        if isPartNumber:
            partNumbers.append(currentNumber)
        
        currentNumber = ""
        isPartNumber = False
        
        for j, cell in enumerate(row):
            if cell.isdigit():
                currentNumber += cell
                for di, dj in NEIGHBOURS_DELTAS:
                    neighbourRow = i + di
                    neighbourCol = j + dj
                    if neighbourRow >= 0 and neighbourRow < len(grid) and neighbourCol >= 0 and neighbourCol < len(row):
                        neighbour = grid[neighbourRow][neighbourCol]
                        if not neighbour.isdigit() and neighbour != ".":
                            isPartNumber = True
            else:
                if isPartNumber:
                    partNumbers.append(currentNumber)
                isPartNumber = False
                currentNumber = ""

    return partNumbers

def main():
    grid = parse(sys.stdin)
    partNumbers = findPartNumbers(grid)
    print(sum(map(int, partNumbers)))

if __name__ == "__main__":
    main()