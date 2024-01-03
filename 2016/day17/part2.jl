using MD5
using AStarSearch

NEIGHBORS = [
    ('U',  -1,  0),
    ('D',  1,  0),
    ('L',  0, -1),
    ('R',  0,  1),
]

OPEN_CODES = "bcdefg"

struct State
    position::Tuple{Int, Int}
    path::AbstractString
end

function openDoors(key::AbstractString, path::AbstractString)::Vector{Bool}
    codes = bytes2hex(md5("$key$path"))[1:4]
    return [c in OPEN_CODES for c in codes]
end

function nextStates(key::AbstractString, state::State)::Vector{State}
    result = Vector{State}()
    open = openDoors(key, state.path)
    i, j = state.position
    for (o, (d, di, dj)) in zip(open, NEIGHBORS)
        ni = i + di
        nj = j + dj
        if o && 0 <= ni < 4 && 0 <= nj < 4
            newPath = state.path * d
            push!(result, State((ni, nj), newPath))
        end
    end
    return result
end

function isGoal(state::State)::Bool
    return state.position == (3, 3)
end

function findMax(key::AbstractString, state::State)::Int
    if isGoal(state)
        return length(state.path)
    end
    m = maximum((findMax(key, ns) for ns in nextStates(key, state)), init=0)
    return coalesce(m, 0)
end

function solve(key::String)
    start = State((0, 0), "")
    return findMax(key, start)
end
println(solve("qzthpkfp"))