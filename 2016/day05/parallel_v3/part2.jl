using MD5

HashResult = Tuple{Int, Char}

const BATCH_SIZE = 1000

function crackPassword(doorId::String)::String
    results::Dict{Int, HashResult} = Dict()
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
    end
    fetch.(Threads.@spawn findHashesInRange() for _ = 1:Threads.nthreads())
    return join(results[i][2] for i = 0:7)
end

const input = "reyedfim"
@time println(crackPassword(input))