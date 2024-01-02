NEIGHBORS = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1],
]

struct Point
    x::Int64
    y::Int64
end

function isOpen(key::Int64, x::Int64, y::Int64)::Bool
    v = key + x*x +2*x*y + 3*x + y + y*y
    return count_ones(v) % 2 == 0
end

function solve(key::Int64, steps::Int)
    function neighbors(point::Point)::Vector{Point}
        results = Vector{Point}()
        for (dx, dy) in NEIGHBORS
            nx = point.x + dx
            ny = point.y + dy
            if nx >= 0 && ny >= 0 && isOpen(key, nx, ny)
                push!(results, Point(nx, ny))
            end 
        end
        return results
    end

    open = Set{Point}()
    distances = Dict{Point, Int64}()

    start = Point(1, 1)
    distances[start] = 0
    push!(open, start)

    while length(open) > 0
        point = pop!(open)
        dp = distances[point]
        for neighbor in neighbors(point)
            nd = get(distances, neighbor, Inf)
            if nd > dp + 1
                distances[neighbor] = dp + 1
                if dp + 1 < steps
                    push!(open, neighbor)
                end
            end
        end
    end
    
    return length(distances)
end

println(solve(1352, 50))
