function mostRepeated(d::Dict{Char, Int})::Char
    return sort(collect(d), rev=true, by=x->x.second)[1].first
end

function solve(lines)::String
    n = length(lines[1])
    counts = [Dict{Char, Int}() for _ = 1:n]

    for line in lines
        for (d, c) in zip(counts, line)
            d[c] = get(d, c, 0) + 1
        end
    end

    return join(mostRepeated(d) for d in counts)
end

println(solve(readlines()))