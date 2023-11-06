movements = split(readline(), ", ")

direction_vectors = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1],
]

function solve()
    direction = 0
    position = [0, 0]
    visited_positions = Set([Tuple(position)])
    for m in movements
        turn = if m[1] == 'R' 1 else -1 end
        distance_txt = chop(m, head=1, tail=0)
        distance = parse(Int64, distance_txt, base=10)
        direction = mod(direction + turn, 4)
        v = direction_vectors[direction + 1]
        while distance > 0
            distance -= 1
            position += v
            if Tuple(position) ∈ visited_positions
                return abs(position[1]) + abs(position[2])
            end
            push!(visited_positions, Tuple(position))
        end
    end
end

println(solve())