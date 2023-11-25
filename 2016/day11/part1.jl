using AStarSearch

@enum ComponentType CHIP = 1 GENERATOR = 2

@enum Direction UP = 1 DOWN = -1

struct Component
    type::ComponentType
    material::Int
end

mutable struct ComponentsLocation
    chipFloor::Int
    generatorFloor::Int
end

function Base.getindex(c::ComponentsLocation, i::ComponentType)::Int
    if i === CHIP
        return c.chipFloor
    else
        return c.generatorFloor
    end
end

function Base.setindex!(c::ComponentsLocation, v::Int, i::ComponentType)::Int
    if i === CHIP
        c.chipFloor = v
    else
        c.generatorFloor = v
    end
end

function Base.isless(a::ComponentsLocation, b::ComponentsLocation)
    return (a.chipFloor => a.generatorFloor) < (b.chipFloor => b.generatorFloor)
end

struct State
    elevatorFloor::Int
    components::Vector{ComponentsLocation}
end

ORDINALS = Dict{AbstractString,Int}(
    "first" => 1,
    "second" => 2,
    "third" => 3,
    "fourth" => 4,
)

GOAL_FLOOR = 4

MaterialsLookup = Dict{AbstractString, Int}

function getMaterialIndex(materials::MaterialsLookup, component::AbstractString)::Int
    n = length(materials) + 1
    return get!(materials, component, n)
end

GENERATOR_EXPRESSION = r"([a-z]+) generator"
MICROCHIP_EXPRESSION = r"([a-z]+)-compatible microchip"

function parseComponents(materials::MaterialsLookup, componentsPart::AbstractString)::Vector{Component}
    result = Vector{Component}()
    for m in eachmatch(GENERATOR_EXPRESSION, componentsPart)
        material = getMaterialIndex(materials, m.captures[1])
        push!(result, Component(GENERATOR, material))
    end
    for m in eachmatch(MICROCHIP_EXPRESSION, componentsPart)
        material = getMaterialIndex(materials, m.captures[1])
        push!(result, Component(CHIP, material))
    end
    return result
end

function parseLine(line::AbstractString, materials::MaterialsLookup)::Pair{Int, Vector{Component}}
    floorPart, componentsPart = split(line, "contains")
    _, floorOrdinal, _ = split(floorPart)
    floor = ORDINALS[floorOrdinal]

    return floor => parseComponents(materials, componentsPart)
end

function parseProblem(lines::Vector{String})::State
    materials = MaterialsLookup()
    sparseFloors = [parseLine(line, materials) for line in lines]
    componentLocations = [ComponentsLocation(-1, -1) for _ in eachindex(materials)]
    for (floor, components) in sort(sparseFloors, by=p->p.first)
        for c in components
            componentLocations[c.material][c.type] = floor
        end
    end

    return State(1, componentLocations)
end

function isValidFloor(components::Vector{ComponentsLocation}, floor::Int)
    hasGenerators = false
    hasChips = false
    unshieldedChips = false
    for component in components
        if component.chipFloor == floor
            hasChips = true
        end
        if component.generatorFloor == floor
            hasGenerators = true
        end
        if component.chipFloor == floor && component.generatorFloor != floor
            unshieldedChips = true
        end
    end

    return !hasChips || !hasGenerators || !unshieldedChips
end


function move(state::State, direction::Direction, components::Vector{Component})::Union{Missing, State}
    destinationFloorNumber = state.elevatorFloor + Int(direction)

    if !(1 <= destinationFloorNumber <= GOAL_FLOOR)
        return missing
    end

    nextStateComponents = deepcopy(state.components)
    for c in components
        nextStateComponents[c.material][c.type] = destinationFloorNumber
    end

    if !isValidFloor(nextStateComponents, destinationFloorNumber) || !isValidFloor(nextStateComponents, state.elevatorFloor)
        return missing
    end

    return State(destinationFloorNumber, sort(nextStateComponents))
end

function currentFloorComponents(state::State)::Vector{Component}
    result = Vector{Component}()
    for (material, c) in enumerate(state.components)
        if c.chipFloor == state.elevatorFloor
            push!(result, Component(CHIP, material))
        end
        if c.generatorFloor == state.elevatorFloor
            push!(result, Component(GENERATOR, material))
        end
    end
    return result
end

function pushNotMissing!(vector, value)
    if value !== missing
        push!(vector, value)
    end
end

function nextStates(state::State)::Set{State}
    result = Set{State}()
    components = currentFloorComponents(state)
    for direction in instances(Direction)
        for i in eachindex(components)
            pushNotMissing!(result, move(state, direction, [components[i]]))
            for j=i:lastindex(components)
                pushNotMissing!(result, move(state, direction, [components[i], components[j]]))
            end
        end
    end
    return result
end

function heuristic(from::State, to::State)::Int
    h = 0
    for (c1, c2) in zip(from.components, to.components)
        h += abs(c1.chipFloor - c2.chipFloor)
        h += abs(c1.generatorFloor - c2.generatorFloor)
    end
    return h
end

function solve(start::State)::Any
    goalComponents = deepcopy(start.components)
    
    for c in goalComponents
        c.chipFloor = GOAL_FLOOR
        c.generatorFloor = GOAL_FLOOR
    end
    
    goal = State(GOAL_FLOOR, goalComponents)

    function isGoal(state::State, _::State)::Bool
        return (state.elevatorFloor == GOAL_FLOOR &&
            all(c.chipFloor == c.generatorFloor == GOAL_FLOOR for c in state.components)
        )
    end

    function hashfn(state::State)::UInt
        return hash(string(state))
    end

    solution = astar(nextStates, start, goal, isgoal=isGoal, hashfn=hashfn, heuristic=heuristic)
    return solution.cost
end

println(solve(parseProblem(readlines())))