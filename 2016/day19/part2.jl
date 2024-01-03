mutable struct Node
    v::Int
    previous::Union{Node, Missing}
    next::Union{Node, Missing}
end

function createRing(elves::Int)
    first = Node(1, missing, missing)
    last = first
    for i = 2:elves
        next = Node(i, last, missing)
        last.next = next
        last = next
    end
    last.next = first
    first.previous = last
    return first
end

function elimination(first::Node, elves::Int)::Int
    opposite = first
    for _ = 1:div(elves, 2)
        opposite = opposite.next
    end
    current = first
    remaining = elves
    while remaining > 1
        skip = opposite

        opposite = opposite.next
        if remaining % 2 == 1
            opposite = opposite.next
        end

        skip.previous.next = skip.next
        skip.next.previous = skip.previous

        current = current.next
        remaining -= 1
    end
    return current.v
end

function solve(elves::Int)::Int
    ring = createRing(elves)
    return elimination(ring, elves)
end

println(solve(3018458))
