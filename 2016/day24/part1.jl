using Combinatorics

NEIGHBORS = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1],
]

Point = Tuple{Int, Int}


function calculateDistances(start::Point, floorMap::Vector{String})::Dict{Pair{Char, Char}, Int}
    i, j = start
    rows = length(floorMap)
    cols = length(first(floorMap))

    s = floorMap[i][j]

    result = Dict{Pair{Char, Char}, Int}()

    distances = Dict{Tuple{Int, Int}, Int}(start => 0)
    open = [(i, j)]

    function neighbors(point::Point)::Vector{Point}
        myNeighbors = Vector{Point}()
        pi, pj = point
        for (di, dj) in NEIGHBORS
            ni = pi + di
            nj = pj + dj
            if 0 < ni <= rows && 0 < nj <= cols && floorMap[ni][nj] != '#'
                push!(myNeighbors, (ni, nj))
            end 
        end
        return myNeighbors
    end


    while length(open) > 0
        point = popfirst!(open)
        dp = distances[point]
        for neighbor in neighbors(point)
            i, j = neighbor
            nd = get(distances, neighbor, Inf)
            if nd > dp + 1
                distances[neighbor] = dp + 1
                if floorMap[i][j] in "0123456789"
                    result[s => floorMap[i][j]] = dp + 1
                end
                push!(open, neighbor)
            end
        end
    end
    return result
end

function calculateNodesDistances(floorMap::Vector{String})::Dict{Pair{Char, Char}, Int}
    distances = Dict{Pair{Char, Char}, Int}()
    for (i, row) in enumerate(floorMap)
        for (j, cell) in enumerate(row)
            if cell in "0123456789"
                merge!(distances, calculateDistances((i,j), floorMap))
            end
        end
    end
    return distances
end

function permutationDistance(perm::Vector{Char}, nodeDistances::Dict{Pair{Char,Char},Int})::Int
    return sum(
        nodeDistances[perm[i-1] => perm[i]]
            for i = 2:length(perm)
    )
end

function solve(floorMap::Vector{String})::Int
    nodeDistances = calculateNodesDistances(floorMap)
    nodes = Set(i for (i, _) in keys(nodeDistances))
    nodesMinusStart = [i for i in nodes if i != '0']
    return minimum(
        permutationDistance(['0'; p], nodeDistances)
            for p in permutations(nodesMinusStart)
    )
end

println(solve(readlines()))