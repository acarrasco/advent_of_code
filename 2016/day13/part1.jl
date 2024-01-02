using AStarSearch

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

function solve(key::Int64, goal::Point)
    function nextStates(point::Point)::Vector{Point}
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
    function heuristic(from::Point, to::Point)::Int64
        return abs(from.x - to.x) + abs(from.y - to.y)
    end

    start = Point(1, 1)

    solution = astar(nextStates, start, goal, heuristic=heuristic)
    return solution.cost
end

println(solve(1352, Point(31, 39)))
