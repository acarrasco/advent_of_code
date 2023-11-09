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
    characters = []
    salt = -1
    while length(characters) < 8
        hash, salt = nextHash(doorId, salt)
        push!(characters, hash[6])
    end
    return join(characters)
end

const input = "reyedfim"
@time begin
    println(crackPassword(input))
end