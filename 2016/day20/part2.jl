struct Range
    from::Int
    to::Int
end

function parseLine(line::AbstractString)::Range
    a, b = split(line, "-")
    return Range(parse(Int, a), parse(Int, b))
end

MAX_RANGE = 4294967295

function solve(blockedRanges::Vector{Range})::Int
    sortedByFrom = sort(blockedRanges, lt=(a, b)->a.from < b.from)
    free = 0
    to = 0
    for r in sortedByFrom
        free += max(0, r.from - to - 1)
        to = max(to, r.to)
    end
    free += max(0, MAX_RANGE - to - 1)
    return free
end

input = map(parseLine, readlines())
println(solve(input))