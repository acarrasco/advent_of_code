using MD5

HashResult = Tuple{Int, String}
HashResults = Vector{HashResult}


function hashesToPassword(hashes::HashResults)::String
    sorted = sort(hashes)[1:8]
    return join(x[6] for (_, x) in sorted)
end

const BATCH_SIZE = 1000

function crackPassword(doorId::String)::String
    results::HashResults = []
    resultsLock = ReentrantLock()
    saltLock = ReentrantLock()
    salt = 0

    function findHashesInRange()
        mySalt = 0
        while length(results) < 8
            lock(saltLock) do
                mySalt = salt
                salt += BATCH_SIZE
            end
            for s = mySalt:mySalt+BATCH_SIZE
                hash = bytes2hex(md5("$doorId$s"))
                if hash[1:5] == "00000"
                    lock(resultsLock) do
                        push!(results, (s, hash))
                    end
                end
            end
        end
    end
    fetch.(Threads.@spawn findHashesInRange() for _ = 1:Threads.nthreads())
    return hashesToPassword(results)
end

const input = "reyedfim"
@time println(crackPassword(input))