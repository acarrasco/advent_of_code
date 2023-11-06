DIRECTIONS = Dict(
    'U' => [-1, 0],
    'R' => [0, 1],
    'D' => [1, 0],
    'L' => [0, -1],
)

function position_to_key(p)
    i, j = p
    n = 1
    for row = -2:i-1
        width = 5 - 2*abs(row)
        n += width
    end
    n += j + 2 - abs(i)
    return "123456789ABCD"[n]
end

function try_move(p, v)
    ni, nj = p + v
    if abs(ni) + abs(nj) <= 2
        return p + v
    else
        return p
    end
end

function solve(lines)
    result = []
    p = [0, -2] # 5
    for line in lines
        for d in line
            p = try_move(p, DIRECTIONS[d])
        end
        key = position_to_key(p)
        push!(result, key)
    end
    return join(result)
end
println(solve(readlines()))
