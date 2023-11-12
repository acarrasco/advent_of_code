function findPatterns(w::AbstractString)::Vector{String}
    results = Vector{String}()
    for i = 1:length(w) - 2
        if w[i] != w[i+1] && w[i] == w[i+2]
            push!(results, w[i:i+2])
        end
    end
    return results
end

withinBrackets::Regex = r"\[[^\]]+\]"

function supportsSSL(ip::String)::Bool
    for m in eachmatch(withinBrackets, ip)
        for p in findPatterns(m.match)
            rp = p[2] * p[1] * p[2]
            for w in split(ip, withinBrackets)
                if occursin(rp, w)
                    return true
                end
            end
        end
    end
    return false
end

println(sum(map(supportsSSL, readlines())))
