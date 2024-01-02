
mutable struct State
    ic::UInt32
    registers::Dict{AbstractString, Int32}
end

cpyExp = r"cpy (-?[0-9]+|[abcd]) ([abcd])"
incExp = r"inc ([abcd])"
decExp = r"dec ([abcd])"
jnzExp = r"jnz ([0-9]+|[abcd]) (-?[0-9]+)"

function extract(state::State, r::AbstractString)::Int32
    value = get(state.registers, r, missing)
    if value === missing
        value = parse(Int, r)
    end
    return value
end

function step(instruction::AbstractString, state::State)
    m = match(cpyExp, instruction)
    if m !== nothing
        value = extract(state, m.captures[1])
        r = m.captures[2]
        state.registers[r] = value
        state.ic += 1
        return
    end
    m = match(incExp, instruction)
    if m !== nothing
        r = m.captures[1]
        state.registers[r] += 1
        state.ic += 1
        return
    end
    m = match(decExp, instruction)
    if m !== nothing
        r = m.captures[1]
        state.registers[r] -= 1
        state.ic += 1
        return
    end
    m = match(jnzExp, instruction)
    if m !== nothing
        r = m.captures[1]
        value = extract(state, r)
        if value != 0
            jump = parse(Int, m.captures[2])
            state.ic += jump
            return
        end
        state.ic += 1
        return
    end
    error("Invalid instruction <$instruction>") 
end

function run(lines::Vector{String})
    state = State(1, Dict(
        "a" => 0,
        "b" => 0,
        "c" => 0,
        "d" => 0,
    ))

    while state.ic <= length(lines)
        step(lines[state.ic], state)
    end

    return state.registers["a"]
end

println(run(readlines()))