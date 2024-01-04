struct Point
    x::Int
    y::Int
end

struct Node
    location::Point
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
    return Node(Point(x, y), size, used, available)
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

NEIGHBORS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

function calculateDistances(start::Point, rows::Int, cols::Int, blocked::Set{Point})
    function neighbors(point::Point)::Vector{Point}
        results = Vector{Point}()
        for (dx, dy) in NEIGHBORS
            nx = point.x + dx
            ny = point.y + dy
            np = Point(nx, ny)
            if 0 <= nx < cols && 0 <= ny < rows && np ∉ blocked
                push!(results, np)
            end 
        end
        return results
    end

    distances = Dict(start => 0)
    open = [start]

    while length(open) > 0
        point = pop!(open)
        currentDistance = distances[point]
        for neighbor in neighbors(point)
            neighborDistance = get(distances, neighbor, Inf)
            if neighborDistance > currentDistance + 1
                distances[neighbor] = currentDistance + 1
                push!(open, neighbor)
            end
        end
    end

    return distances
end

function solve(nodes::Vector{Node})::Int
    blocked = Set{Point}()
    empty = missing
    maxX = 0
    maxY = 0
    for node in nodes
        maxX = max(maxX, node.location.x)
        maxY = max(maxY, node.location.y)
        if node.size > 100
            push!(blocked, node.location)
        end
        if node.used == 0
            empty = node.location
        end
    end
    d = calculateDistances(Point(maxX, 0), maxY+1, maxX+1, blocked)
    terminal = Point(0, 0)
    return d[empty] + 5 * (d[terminal] - 1)
end


input = parseInput(readlines())
println(solve(input))