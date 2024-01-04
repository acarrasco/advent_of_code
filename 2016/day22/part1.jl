struct Node
    x::Int
    y::Int
    size::Int
    used::Int
    available::Int
end

NODE_EXP = r"/dev/grid/node-x([0-9]+)-y([0-9]+)[ ]+([0-9]+)T[ ]+([0-9]+)T[ ]+([0-9]+)T[ ]+[0-9]+%"

function parseLine(line::AbstractString)::Union{Node, Nothing}
    m = match(NODE_EXP, line)
    if m === nothing
        return nothing
    end
    x = parse(Int, m.captures[1])
    y = parse(Int, m.captures[2])
    size = parse(Int, m.captures[3])
    used = parse(Int, m.captures[4])
    available = parse(Int, m.captures[5])
    return Node(x, y, size, used, available)
end

function parseInput(lines::Vector{String})::Vector{Node}
    result = Vector()
    for line in lines
        node = parseLine(line)
        if node !== nothing
            push!(result, node)
        end
    end
    return result
end

function solve(nodes::Vector{Node})::Int
    result = 0
    for a in nodes
        for b in nodes
            if a !== b && a.used > 0 && a.used <= b.available
                println("a:$a -> b:$b")
                result += 1
            end
        end
    end
    return result
end

input = parseInput(readlines())
println(solve(input))