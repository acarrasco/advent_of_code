

function rotateRow!(mat::Matrix, row::Int, amount::Int)
    r = mat[row, :]
    mat[row, :] = [r[(i - amount + length(r)) % length(r) + 1] for i=0:length(r)-1]
    return mat
end

function rotateColumn!(mat::Matrix, column::Int, amount::Int)
    c = mat[:, column]
    mat[:, column] = [c[(i - amount +  length(c)) % length(c) + 1] for i=0:length(c)-1]
    return mat
end

function fillRect!(mat::Matrix, value, rows::Int, cols::Int)
    mat[1:rows, 1:cols].= value
    return mat
end

function solve(input)
    rect = zeros(Int8, 6, 50)
    for line in input
        command, args... = split(line)
        if command == "rect"
            cols, rows = split(args[1], "x")
            fillRect!(rect, 1, parse(Int, rows), parse(Int, cols))
        elseif command == "rotate" && args[1] == "row"
            row = parse(Int, split(args[2], "=")[2]) + 1
            amount = parse(Int, args[4])
            rotateRow!(rect, row, amount)
        elseif command == "rotate" && args[1] == "column"
            col = parse(Int, split(args[2], "=")[2]) + 1
            amount = parse(Int, args[4])
            rotateColumn!(rect, col, amount)
        end
    end

    d = Dict(
        0 => " ",
        1 => "*"
    )

    for row in eachrow(rect)
        println(join(d[x] for x in row))
    end
end

solve(readlines())