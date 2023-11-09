using MD5

HashResult = Tuple{Int, String}
HashResults = Vector{HashResult}

function findHashesInRange(doorId::String, saltFrom::Int, saltTo, results:: HashResults, resultsLock)
    for salt = saltFrom:saltTo
        hash = bytes2hex(md5("$doorId$salt"))
        if hash[1:5] == "00000"
            lock(resultsLock) do
                push!(results, (salt, hash))
            end
        end
    end
end

function hashesToPassword(hashes::HashResults)::String
    sorted = sort(hashes)[1:8]
    return join(x[6] for (_, x) in sorted)
end

const BATCH_SIZE = 100000

function crackPassword(doorId::String)::String
    results::HashResults = []
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
    return hashesToPassword(results)
end

const input = "reyedfim"
@time println(crackPassword(input))