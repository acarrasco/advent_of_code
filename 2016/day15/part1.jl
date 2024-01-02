
struct Disc
    period::Int
    offset::Int
end

function parse_line(line::AbstractString)::Disc
    tokens = split(line)
    period = parse(Int, tokens[4])
    offset = parse(Int, chop(tokens[12]))
    return Disc(period, offset)
end

function solve(discs::AbstractVector{Disc})
    period = 1
    for disc in discs
        period *= disc.period
    end
    offset = 0
    for (i, disc) in enumerate(discs)
        m = div(period, disc.period)
        offset += (i + disc.offset) * m * invmod(m, disc.period)
    end
    return period - (offset % period)
end

discs = map(parse_line, readlines())
println(solve(discs))