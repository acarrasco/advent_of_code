using MD5

function nextHash(doorId::String, salt::Int):: Tuple{String, Int}
    while true
        salt += 1
        hash = bytes2hex(md5("$doorId$salt"))
        if hash[1:5] == "00000"
            return hash, salt
        end
    end
end

function crackPassword(doorId::String)::String
    characters = Dict{Int, Char}()
    salt = -1
    while length(characters) < 8
        hash, salt = nextHash(doorId, salt)
        p = parse(Int, hash[6], base=16)
        if p < 8 && p ∉ keys(characters)
            characters[p] = hash[7]
        end
    end
    return join(characters[i] for i = 0:7)
end

const input = "reyedfim"
@time println(crackPassword(input))