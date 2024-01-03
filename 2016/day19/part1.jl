mutable struct Node
    v::Int
    next::Union{Node, Missing}
end

function createRing(elves::Int)
    first = Node(1, missing)
    last = first
    for i = 2:elves
        next = Node(i, missing)
        last.next = next
        last = next
    end
    last.next = first
    return first
end

function elimination(first::Node)::Int
    current = first
    while current.next !== current
        skip = current.next
        current.next = skip.next
        current = skip.next    
    end
    return current.v
end

function solve(elves::Int)::Int
    ring = createRing(elves)
    return elimination(ring)
end

println(solve(3018458))
