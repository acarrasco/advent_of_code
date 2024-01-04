function isTrap(left::Bool, right::Bool)::Bool
    return xor(left, right)
end

function nextRow(row::BitVector)::BitVector
    padded = [false; row; false]
    return [isTrap(padded[i-1], padded[i+1]) for i = 2:length(row)+1]
end

function parse(line::AbstractString)::BitVector
    return [c=='^' for c in strip(line)]
end

function solve(firstRow::BitVector, rows::Int)::Int
    c = 0
    row = firstRow
    for _ = 1:rows
        c += length(row) - sum(row)
        row = nextRow(row)
    end
    return c
end

input = parse(readline())
println("Part1: $(solve(input, 40))")
println("Part2: $(solve(input, 400000))")
