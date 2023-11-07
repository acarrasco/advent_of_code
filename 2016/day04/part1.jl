struct RoomCode
    encryptedName::AbstractString
    sector::Int
    hash::AbstractString
end

function parseRoom(txt::AbstractString)::RoomCode
    content, hash = split(txt, "[")
    hash = chop(hash, head=0, tail=1)
    encryptedName, sector = rsplit(content, "-", limit=2)
    return RoomCode(encryptedName, parse(Int, sector), hash)
end

function calculateHash(room::RoomCode)
    charCounts = Dict{Char, Int}()
    for c in room.encryptedName
        if c != '-'
            charCounts[c] = get(charCounts, c, 0) + 1
        end
    end
    key(x) = (-charCounts[x], x)
    sortedChars = sort(collect(keys(charCounts)), by=key)
    return join(sortedChars[1:5])
end

validHash(room::RoomCode) = calculateHash(room) == room.hash

function solve()
    roomCodes = map(parseRoom, readlines())
    validRooms = filter(validHash, roomCodes)
    return sum(room.sector for room in validRooms)
end

println(solve())