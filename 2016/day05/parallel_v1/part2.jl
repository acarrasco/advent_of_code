using Distributed
@everywhere include("./hash.jl")
using .hash

const BATCH_SIZE = 10000000

function crackPassword(doorId::String)::String
    characters = Dict{Int, Char}()
    salt = 0
    while length(characters) < 8
        newHashes = @distributed append! for salt = salt:salt+BATCH_SIZE
            hash.isValidHash(doorId, salt)
        end
        salt += BATCH_SIZE
        for (_, hash) in sort(newHashes)
            p = parse(Int, hash[6], base=16)
            if p < 8 && p ∉ keys(characters)
                characters[p] = hash[7]
            end
        end
    end
    return join(characters[i] for i = 0:7)
end

const input = "reyedfim"
@time println(crackPassword(input))
