struct Range
    from::Int
    to::Int
end

function parseLine(line::AbstractString)::Range
    a, b = split(line, "-")
    return Range(parse(Int, a), parse(Int, b))
end

function solve(blockedRanges::Vector{Range})::Int
    sortedByFrom = sort(blockedRanges, lt=(a, b)->a.from < b.from)
    i = 1
    to = sortedByFrom[1].to
    while sortedByFrom[i].from <= to + 1
        to = max(to, sortedByFrom[i].to)
        i+=1
    end
    return to + 1
end

input = map(parseLine, readlines())
println(solve(input))