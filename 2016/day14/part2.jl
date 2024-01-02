using MD5
using DataStructures

function consecutive(txt::AbstractString, n::Int)::Union{Char, Missing}
    for i = 1:length(txt) - n + 1
        c = txt[i]
        if all(txt[j] == c for j=i+1:i+n-1)
            return c
        end
    end
    return missing
end

LOOKAHEAD = 1000
NEEDED = 64
FIRST_CONSECUTIVE = 3
NEXT_CONSECUTIVE = 5
REPEAT_HASH = 2016

function stretched_hash(salt::AbstractString, i::Int)::AbstractString
    hash = bytes2hex(md5("$salt$i"))
    for i = 1:REPEAT_HASH
        hash = bytes2hex(md5(hash))
    end
    return hash
end

function solve(salt::AbstractString)::UInt64
    buffer = CircularBuffer(LOOKAHEAD)
    for i = 1:LOOKAHEAD
        push!(buffer, stretched_hash(salt, i))
    end

    remaining = NEEDED
    i = 0
    while remaining > 0
        i += 1
        h = popfirst!(buffer)
        push!(buffer, stretched_hash(salt, i+LOOKAHEAD))
        c = consecutive(h, FIRST_CONSECUTIVE)
        if c !== missing
            rc = repeat(c, NEXT_CONSECUTIVE)
            if any(contains(nh, rc) for nh in buffer)
                remaining -= 1
            end
        end
    end
    return i
end

println(solve("jlmsuwbz"))
# println(solve("abc"))