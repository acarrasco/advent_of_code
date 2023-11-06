DIRECTIONS = Dict(
    'U' => [-1, 0],
    'R' => [0, 1],
    'D' => [1, 0],
    'L' => [0, -1],
)

function position_to_key(p)
    i, j = p
    return i * 3 + j + 1
end

function solve(lines)
    result = []
    p = [1, 1]
    for line in lines
        for d in line
            p += DIRECTIONS[d]
            clamp!(p, 0, 2)
        end
        key = position_to_key(p)
        push!(result, key)
    end
    return join(result)
end
println(solve(readlines()))
