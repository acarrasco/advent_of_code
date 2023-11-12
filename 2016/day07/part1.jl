function hasPattern(w::AbstractString):Bool
    for i = 1:length(w) - 3
        if w[i] != w[i+1] && w[i] == w[i+3] && w[i+1] == w[i+2]
            return true
        end
    end
    return false
end

withinBrackets::Regex = r"\[[^\]]+\]"

function supportsTLS(ip::String)::Bool
    for m in eachmatch(withinBrackets, ip)
        if hasPattern(m.match)
            return false
        end
    end
    for w in split(ip, withinBrackets)
        if hasPattern(w)
            return true
        end
    end
    return false
end

println(sum(map(supportsTLS, readlines())))
