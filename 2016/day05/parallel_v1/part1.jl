using Distributed
@everywhere include("./hash.jl")
using .hash

function hashesToPassword(hashes::HashResults)::String
    sorted = sort(hashes)[1:8]
    return join(x[6] for (_, x) in sorted)
end

const BATCH_SIZE = 100000

function crackPassword(doorId::String)::String
    hashes::HashResults = []
    salt = 0
    while length(hashes) < 8
        newHashes = @distributed append! for salt = salt:salt+BATCH_SIZE
            hash.isValidHash(doorId, salt)
        end
        salt += BATCH_SIZE
        append!(hashes, newHashes)
    end
    return hashesToPassword(hashes)
end

const input = "reyedfim"
@time println(crackPassword(input))