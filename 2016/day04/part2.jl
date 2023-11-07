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

function calculateHash(room::RoomCode)::String
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

A_CODE = Int('a')
Z_CODE = Int('z')
ALPHABET_SIZE = Z_CODE - A_CODE + 1

shift(c::Char, n::Int)::Char = Char(A_CODE + (Int(c) - A_CODE + n) % ALPHABET_SIZE)

function decryptName(room::RoomCode)::String
    mapCharacter(c) = if c == '-' ' ' else shift(c, room.sector) end
    return join(map(mapCharacter, room.encryptedName))
end

function solve()
    roomCodes = map(parseRoom, readlines())
    validRooms = filter(validHash, roomCodes)
    for room in validRooms
        name = decryptName(room)
        if occursin("north", name)
            return room.sector
        end
    end
end

println(solve())