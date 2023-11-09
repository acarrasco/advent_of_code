module hash
    using MD5

    export isValidHash
    export HashResult
    export HashResults

    HashResult = Tuple{Int, String}
    HashResults = Vector{HashResult}

    const none = []

    function isValidHash(doorId::String, salt::Int):: HashResults
        hash = bytes2hex(md5("$doorId$salt"))
        if hash[1:5] == "00000"
            return [(salt, hash)]
        end
        return none
    end

end