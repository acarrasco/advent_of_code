using MD5

HashResult = Tuple{Int, Char}

function findHashesInRange(doorId::String, saltFrom::Int, saltTo, results:: Dict{Int, HashResult}, resultsLock)
    for salt = saltFrom:saltTo
        hash = bytes2hex(md5("$doorId$salt"))
        if hash[1:5] == "00000"
            p = parse(Int, hash[6], base=16)
            if p < 8
                lock(resultsLock) do
                    if p ∉ keys(results) || salt < results[p][1]
                        results[p] = (salt, hash[7])
                    end
                end
            end
        end
    end
end

const BATCH_SIZE = 100000

function crackPassword(doorId::String)::String
    results::Dict{Int, HashResult} = Dict()
    resultsLock = ReentrantLock()
    salt = 0
    while length(results) < 8
        tasks = []
        for _ = 1:Threads.nthreads()
            push!(tasks, Threads.@spawn findHashesInRange(doorId, $salt, $salt + BATCH_SIZE, results, resultsLock))
            salt += BATCH_SIZE
        end
        fetch.(tasks)
    end
    return join(results[i][2] for i = 0:7)
end

const input = "reyedfim"
@time println(crackPassword(input))