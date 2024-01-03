function extend(a::BitVector)::BitVector
    b = .! reverse(a)
    return [a; false; b] # a 0 would cast the whole thing to Int
end

function byPairs(v::AbstractVector)
    halfLength = div(length(v),2)
    return (v[2*i-1] => v[2*i] for i = 1:halfLength)
end

function checksum(v::BitVector)::BitVector
    s = v
    while length(s) % 2 != 1
        s = [a == b for (a, b) in byPairs(s)]
    end
    return s
end

function pad(seed::BitVector, n::Int)::BitVector
    v = seed
    while length(v) < n
        v = extend(v)
    end
    return v[1:n]
end

function solve(seed::String, n::Int)::BitVector
    v = BitVector(a == '1' for a in seed)
    padding = pad(v, n)
    return checksum(padding)
end

function format(v::BitVector)::String
    return join(Int(i) for i in v)
end

part1 = format(solve("01111010110010011", 272))
println("Part1: $part1")
part2 = format(solve("01111010110010011", 35651584))
println("Part2: $part2")